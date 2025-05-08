import azure.functions as func
from azure.functions.decorators.core import DataType
import logging, os
import json
from datetime import datetime, UTC
from azure.storage.blob import BlobServiceClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.face import FaceAdministrationClient, FaceClient
from azure.ai.vision.face.models import FaceAttributeTypeRecognition04, FaceDetectionModel, FaceRecognitionModel, QualityForRecognition
from azure.ai.vision.face.models import LargePersonGroupPerson
import pytz

# ─── CONFIG from ENV ─────────────────────────────────────────────────────
KEY = os.getenv("FACE_APIKEY")
ENDPOINT = os.getenv("FACE_ENDPOINT")
beirut_tz = pytz.timezone('Asia/Beirut')

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.generic_output_binding(
    arg_name="AttendanceTable",
    type="sql",
    CommandText="dbo.Attendance",
    ConnectionStringSetting="SqlConnectionString",
    data_type=DataType.STRING
)

@app.sql_input(
    arg_name="schedule",
    command_text=f"select [id], [course_code] from dbo.Schedules where class = @class and session_start <= '{datetime.now(beirut_tz).strftime('%Y-%m-%d %H:%M:%S')}' and session_end >= '{datetime.now(beirut_tz).strftime('%Y-%m-%d %H:%M:%S')}'",
    command_type="Text",
    parameters="@class={class}",
    connection_string_setting="SqlConnectionString"
)

@app.route(route="handleAttendance/{class}", methods=["POST"])
def handleAttendance(
    req: func.HttpRequest, 
    AttendanceTable: func.Out[func.SqlRow],
    schedule: func.SqlRowList
) -> func.HttpResponse:
    logging.info(f"Received image upload request")
    image = req.get_body()

    if not image:
        return func.HttpResponse("No image provided", status_code=400)

    LARGE_PERSON_GROUP_ID = str('i4test')

    with FaceAdministrationClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY)) as face_admin_client, \
        FaceClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY)) as face_client:

        schedules = list(map(lambda r: json.loads(r.to_json()), schedule))

        if not schedules:
            return func.HttpResponse("No schedules now", status_code=200)

        # Detect faces
        face_ids = []
        # We use detection model 03 to get better performance, recognition model 04 to support quality for
        # recognition attribute.
        faces = face_client.detect(
            image_content=image,
            detection_model=FaceDetectionModel.DETECTION03,
            recognition_model=FaceRecognitionModel.RECOGNITION04,
            return_face_id=True,
            return_face_attributes=[FaceAttributeTypeRecognition04.QUALITY_FOR_RECOGNITION],
        )
        for face in faces:
            # Only take the face if it is of sufficient quality.
            if face.face_attributes.quality_for_recognition != QualityForRecognition.LOW:
                face_ids.append(face.face_id)
            else:
                return func.HttpResponse("Image quality not sufficient", status_code=400)

        # Identify faces
        identify_results = face_client.identify_from_large_person_group(
            face_ids=face_ids,
            large_person_group_id=LARGE_PERSON_GROUP_ID,
        )

        for identify_result in identify_results:
            if identify_result.candidates:

                # Verify faces
                verify_result = face_client.verify_from_large_person_group(
                    face_id=identify_result.face_id,
                    large_person_group_id=LARGE_PERSON_GROUP_ID,
                    person_id=identify_result.candidates[0].person_id,
                )
                logging.info(f"verification result: {verify_result.is_identical}. confidence: {verify_result.confidence}")

                person: LargePersonGroupPerson = face_admin_client.large_person_group.get_person(
                    large_person_group_id=LARGE_PERSON_GROUP_ID,
                    person_id=identify_result.candidates[0].person_id
                )

                schedule_data = dict(schedules[0])

                logging.info(f"id: {schedule_data['id']}, course_code: {schedule_data['course_code']}")

                AttendanceTable.set(
                    func.SqlRow({
                        "schedule_id": schedule_data['id'],
                        "student_id": person.name,
                        "course_code": schedule_data['course_code'],
                        "arrival_time": datetime.now(beirut_tz).strftime('%Y-%m-%d %H:%M:%S')
                    })
                )
                    
                logging.info(f"Srudent with the Id = {person.name} saved to the Attendance table")

                payload = {
                    "verification_result": verify_result.is_identical,
                    "confidence": verify_result.confidence,
                    "person": person.name
                }
                
                return func.HttpResponse(
                    body=json.dumps(payload),
                    status_code=200,
                    mimetype="application/json"
                )
            
            else:
                return func.HttpResponse(f"No person identified for face ID {identify_result.face_id} in image.", status_code=400)