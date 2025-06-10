# Handle Attendance - Azure Function

This **Azure Function** performs automated student attendance logging using **Azure Face API** for facial recognition. Upon receiving a student's face image, the function:

1. Verifies if the current time matches any active session.
2. Detects and identifies the student using the **Face API**.
3. If identified and verified, logs the student's attendance in the **Azure SQL Database**.

---

## 📌 Function Overview

- **Trigger Type:** HTTP (anonymous)
- **Method:** POST
- **Route:** `/handleAttendance`
- **Consumes:** Binary image as request body (`image/jpeg` or `image/png`)
- **Writes to DB:**  
  - Reads from `dbo.Schedules` and `dbo.Attendance` using direct SQL queries via `pymssql`  
  - Inserts into `dbo.Attendance` using **SQL output binding**

---

## 🧠 How It Works

### 🔄 Workflow

1. **Image Upload & Parameters**
   - Receives binary image in the body.
   - Expects `cur_class` as a query parameter (e.g., `CS101`).

2. **Active Session Validation**
   - Queries `dbo.Schedules` to find a class session where the current time falls within ±10 to +30 minutes of `session_start`.

3. **Face Detection & Quality Check**
   - Uses `FaceClient.detect` to ensure one high-quality face is present.

4. **Identification & Verification**
   - Identifies the face against the **Azure Face API** Person Group for the given class.
   - Verifies the face using `verify_from_large_person_group`.

5. **Attendance Logging**
   - Checks if attendance already exists in `dbo.Attendance`.
   - If not, inserts a new row via SQL output binding (`@app.generic_output_binding`).

---

## 🧪 Input & Output

### Request

**POST** `/api/handleAttendance?cur_class=CS101`  
**Headers:** `Content-Type: image/jpeg`  
**Body:** Binary image

### Response

- `200 OK`: JSON payload with verification result, confidence, and student ID.
- `400 Bad Request`: For errors like:
  - No image provided
  - No class in session
  - Face not detected or poor quality
  - Face not recognized
  - Attendance already logged

---

## 🔐 Face API Configuration

- **Recognition Model:** `RECOGNITION04`
- **Detection Model:** `DETECTION03`
- **Quality Check:** Accepts only `QualityForRecognition.HIGH`

---

## 🗃️ Database Access

### 1. **Direct SQL Access via `pymssql`**
- Read operations:
  - `SELECT` from `dbo.Schedules` to find current sessions
  - `SELECT` from `dbo.Attendance` to check existing entries

### 2. **Write via SQL Output Binding**
- Insert operation:
  - Writes new attendance records into `dbo.Attendance` using `@app.generic_output_binding`.

---

## 🧪 Local Development

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Setup local.settings.json:
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "FACE_APIKEY": "<your-api-key>",
    "FACE_ENDPOINT": "<your-face-api-endpoint>",
    "DB_SERVER": "<your-db-server>",
    "DB_USER": "<your-db-username>",
    "DB_PASSWORD": "<your-db-password>",
    "DB_NAME": "<your-db-name>",
    "DB_PORT": "1433",
    "SqlConnectionString": "Server=...;Initial Catalog=...;User ID=...;Password=...;Encrypt=True;"
  }
}
```

3. Run the function
```bash
func start
```

## Refrences:
- [Azure Face API](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview-identity)
- [Azure Functions Python Developer Guide](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python)
- [Azure SQL Output Binding for Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-add-output-binding-azure-sql-vs-code?pivots=programming-language-python#update-your-function-app-settings)
- [pymssql Documentation](https://www.pymssql.org/en/stable/)