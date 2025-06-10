# Schedules Portal

**Schedules Portal** is a modern university portal web application designed to streamline academic management for both students and instructors. Built with **React**, **TypeScript**, **Vite**, and **Chakra UI**, it delivers a fast, accessible, and visually appealing experience. The portal integrates with **Azure Static Web Apps** and **Azure SQL Database** (via Data API Builder) to provide real-time data and secure authentication.

---

## What Does Schedules Portal Do?

Schedules Portal serves as a centralized platform for managing university schedules. It is tailored to the needs of both students and instructors, offering distinct dashboards and workflows for each role.

### Key Features

- 🔐 **Authentication**  
  Secure login for students and instructors, ensuring personalized access to dashboards and data.

- 🧑‍🎓 **Student Dashboard**  
  Students can view their class schedules and session details in a clear, organized interface.

- 👨‍🏫 **Instructor Dashboard**  
  Instructors can manage their teaching schedules, create or delete class sessions, and view all assigned courses.

- 📅 **Schedule Management**  
  Both students and instructors benefit from up-to-date scheduling, with the ability to see upcoming sessions, class times, and course assignments.

- ☁️ **Cloud Integration**  
  The app is deployed on Azure Static Web Apps, with seamless integration to Azure SQL Database for persistent, scalable data storage.

- 🔄 **CI/CD with GitHub Actions**  
  Every push to the `main` branch triggers a GitHub Actions workflow that builds and deploys the app automatically to Azure Static Web Apps.

- 🧪 **Local Development with Azure SWA CLI**  
  The Azure SWA CLI is used to emulate the full stack locally, allowing developers to test the frontend, APIs, and authentication together before deploying.

- 🎨 **Modern UI**  
  Chakra UI provides a responsive, accessible, and themeable component library, ensuring a consistent and user-friendly experience.

- ⚡ **Performance**  
  Powered by Vite, Schedules Portal offers instant hot module reloading and fast build times for a smooth development and user experience.

- 🧹 **Code Quality**  
  TypeScript and ESLint are used throughout the project to maintain high code quality and reliability.

---

## How It Works

- **Role-Based Access:**  
  Users log in as either students or instructors. The portal detects the role and presents the appropriate dashboard and features.

- **Data Integration:**  
  All user, schedule, and course data is managed through Azure SQL Database, accessed securely via Azure Data API Builder.

- **Cloud-Ready Deployment:**  
  The project is deployed to Azure Static Web Apps with automated GitHub Actions CI/CD pipelines. Local development is streamlined using the Azure SWA CLI, which simulates the cloud environment (frontend, APIs, and auth) on your machine.

---

## Technology Stack

- **Frontend:** React, TypeScript, Chakra UI, Vite
- **Backend/Data:** Azure Static Web Apps, Azure SQL Database, Data API Builder
- **DevOps:** GitHub Actions (CI/CD), Azure SWA CLI

---

## Use Cases

- **Students:**

  - Instantly view upcoming classes and session details

- **Instructors:**
  - Manage and update class schedules
  - Create or delete sessions as needed

---

## Project Structure

The codebase is organized for clarity and scalability, with separate folders for components, services, authentication, and type definitions. Configuration files for Azure deployment, CI/CD via GitHub Actions, and local development with SWA CLI are included.

---

## Learn More

- [React Documentation](https://react.dev/)
- [Chakra UI](https://chakra-ui.com/)
- [Vite](https://vite.dev/)
- [Azure Static Web Apps](https://learn.microsoft.com/en-us/azure/static-web-apps/)
- [Azure SWA CLI](https://azure.github.io/static-web-apps-cli/)
- [GitHub Actions for SWA](https://learn.microsoft.com/en-us/azure/static-web-apps/github-actions-workflow)
