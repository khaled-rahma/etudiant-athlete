
```markdown
# Student Athlete Management System (SAMS)

## Project Overview

The Student Athlete Management System (SAMS) is a comprehensive web-based platform developed as a Pluridisciplinary Project for the 4th year Artificial Intelligence Engineering program at Kasdi Merbah University – Ouargla. The system digitizes and automates the entire lifecycle of student participation in official sports and cultural competitions, from registration and invitation management to absence tracking and AI-powered medical document analysis.

## Author Information

- **University**: Kasdi Merbah University – Ouargla (UKMO)
- **Faculty**: Faculty of New Technologies of Information and Communication (FNTIC)
- **Department**: Department of Computer Science
- **Program**: 4th Year Artificial Intelligence Engineering
- **Project Type**: Pluridisciplinary Project
- **Contact Email**: khaledrahmawork@gmail.com

## Problem Statement

In Algerian higher education, students participating in official sports or cultural competitions are entitled to have their absences officially justified by the Ministry of Higher Education. However, the practical implementation has historically been fragmented, inconsistent, and heavily dependent on manual administrative procedures.

**Key Problems:**

1. Lack of a formal tracking system for competition-related absences
2. Manual documentation prone to loss and errors
3. Communication gaps between administrative offices and students
4. No systematic follow-up for absence compensation
5. Data fragmentation across paper forms and individual office records
6. No formal mechanism for injury reporting
7. Administrative overload for Service Managers and Department Heads

## Solution Overview

SAMS provides a full-stack web application that addresses all identified problems through an integrated digital platform with four distinct user roles and AI-powered features.

## Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| Django | 6.0 | Backend MVC Framework |
| SQLite | Built-in | Relational Database (Development) |
| HTML5 | - | Frontend Structure |
| CSS3 | - | Frontend Styling |
| JavaScript | ES6+ | Client-side Interactivity |
| Font Awesome | 6.x | UI Iconography |
| Google Gemini API | 2.5 Flash | AI-powered Injury Analysis |
| Python | 3.10+ | Programming Language |

## User Roles and Permissions

### 1. Student
- Register in the system with personal information
- Upload academic schedule and profile photo
- Respond to competition invitations (accept/refuse)
- Confirm return from competitions
- Report health status (healthy/injured/sick)
- Use AI injury analysis tool
- View personal digital card
- View competition history

### 2. Service Manager
- Approve or reject student registrations
- Receive competition notifications
- Send participation invitations to eligible students
- View all competition results
- Send final reports to Department Head and Vice President
- Monitor all system activities

### 3. Department Head
- View all approved students
- Monitor justified absences
- Receive injury reports
- Access AI-generated injury insights
- View individual student injury reports

### 4. Vice President
- View all approved students
- Monitor justified absences across all departments
- Receive final competition reports
- Access institutional-level analytics

## System Workflow (10 Steps)

**Step 1 - Student Registration:** Student submits registration form including personal information, blood type, specialty, activity category (sports/cultural), specific activity name, photo, and academic schedule. Status is 'pending'.

**Step 2 - Service Manager Review:** Service Manager reviews pending applications. Upon approval, system automatically creates user account with registration number as both username and default password.

**Step 3 - Competition Submission:** Official entity accesses public form and submits competition details including activity type, dates, and location.

**Step 4 - Competition Reception:** Service Manager views incoming competitions. System displays how many eligible students match the competition's activity type and name.

**Step 5 - Invitation Dispatch:** Upon confirming reception, system automatically identifies all approved students matching the competition's activity and creates Participation records with 'pending' status.

**Step 6 - Student Response:** Students log into dashboard and respond to pending invitations (accepting or refusing). System timestamps each response.

**Step 7 - Absence Registration:** When Service Manager sends final participation report, system automatically generates Absence records for all students who accepted, covering full competition date range, with justified status set to True.

**Step 8 - Return Confirmation:** After competition ends, each participating student confirms return through dashboard and reports health status: healthy, injured, or sick.

**Step 9 - AI-Powered Injury Analysis:** AI analyzes uploaded medical file (images and/or description) and generates structured information including Injury Summary, Academic Impact Assessment, Recovery Plan, Return Prediction, Medical Warnings, and Recommendation Summary.

**Step 10 - Reporting:** Department Head and Vice President access real-time dashboards showing all justified absences and AI-generated injury reports.

## Database Models Description

The system is built around five core database models:

**Student Model:** Stores all registered student athletes and cultural participants. Includes fields for personal information (name, registration number, date of birth, blood type, email), academic specialization, activity category (sports or cultural), specific activity name, profile photo, academic schedule, and approval status.

**User Model:** Extends Django's AbstractUser to include role-based access control. Supports four roles: student, service manager, department head, and vice president.

**Competition Model:** Records all competitions received from official entities. Includes activity type, activity name, competition title, location, start date, end date, travel status, and processing status.

**Participation Model:** Tracks student responses to competition invitations. Links students to competitions with status options: pending, accepted, or refused. Includes timestamp of when the student responded.

**Absence Model:** Records justified absences and post-competition health reports. Includes competition date range, return confirmation status, injury status (healthy, injured, or sick), injury description, AI analysis results, and justification status.

## AI-Powered Injury Analysis

Upon confirming their return from a competition, the student can upload a medical image (X-ray or medical report) and/or provide a text description of their injury. The system sends this multimodal input to Google's Gemini 2.5 Flash API, which returns a structured report containing:

- Injury type classification
- Severity percentage (0-100)
- Severity level (Low, Medium, or High)
- Required rest days
- Rehabilitation exercises list
- Nutritional advice
- Return prediction timeline
- Medical warnings
- Academic impact assessment
- Recommendation summary

The AI-generated report is immediately displayed to the student and saved to the database for future reference. The Department Head can access individual student injury reports through the "Justified Absences" interface.

## System Architecture

The system follows a client-server architecture with Django as the backend MVC framework. The frontend consists of HTML5, CSS3, and JavaScript for user interfaces. SQLite serves as the database engine during development. The Google Gemini API is integrated for intelligent analysis of medical documents. The system implements role-based access control with four distinct user roles, each with carefully defined permissions and dedicated dashboard views.

## Project Structure

The project is organized into the following directories and files:

**Root Directory:** Contains manage.py for Django management commands, requirements.txt for dependencies, .env for environment variables, and README.md for documentation.

**Project Configuration Directory (sams/):** Contains settings.py for project configuration, urls.py for URL routing, wsgi.py for deployment, and asgi.py for asynchronous support.

**Applications Directory (apps/):** Contains six Django apps:

- accounts: User authentication and role-based access control
- students: Student registration, profiles, and management
- competitions: Competition submission and management
- participations: Invitation tracking and student responses
- absences: Absence records and injury reporting
- ai_analysis: Google Gemini API integration for medical document analysis

**Templates Directory:** Contains HTML templates organized by app, including base templates, login pages, dashboards, registration forms, competition forms, absence views, and AI analysis interfaces.

**Static Directory:** Contains CSS files for styling, JavaScript files for client-side interactivity, and images for the user interface.

**Media Directory:** Stores user-uploaded files including student photos, academic schedules, and medical documents.

## Installation Instructions

**Prerequisites:**
- Python 3.10 or higher
- Git
- Google Gemini API key for AI features

**Installation Steps:**

First, clone the repository from GitHub to your local machine. Then, navigate into the project directory. Create a virtual environment to isolate project dependencies. Activate the virtual environment (command varies by operating system). Install all required dependencies from the requirements.txt file. Create a .env file to store environment variables including your Django secret key, debug mode setting, and Gemini API key. Run database migrations to create the necessary tables. Create a superuser account to access the admin panel. Collect static files for production. Finally, run the development server to start the application.

**Access Points:**
- Main Application: http://127.0.0.1:8000
- Admin Panel: http://127.0.0.1:8000/admin
- Public Competition Form: http://127.0.0.1:8000/competitions/add/

## API Endpoints Summary

The system provides the following API endpoints:

- Login endpoint for user authentication (GET/POST, public access)
- Logout endpoint for ending user sessions (POST, authenticated users only)
- Dashboard endpoint for role-specific home pages (GET, authenticated users)
- Student registration endpoint for new student submissions (POST, students)
- Pending registrations endpoint for viewing unapproved students (GET, service manager only)
- Student approval endpoint for confirming registrations (POST, service manager only)
- Competition submission endpoint for public competition entries (POST, public access)
- Incoming competitions endpoint for viewing pending competitions (GET, service manager only)
- Competition confirmation endpoint for approving competitions (POST, service manager only)
- Competition results endpoint for viewing final outcomes (GET, service manager only)
- Invitation response endpoint for student replies (POST, students only)
- Justified absences endpoint for viewing absence records (GET, department head and vice president)
- Return confirmation endpoint for post-competition return (POST, students only)
- AI injury analysis endpoint for medical document processing (POST, students only)
- AI report endpoint for viewing injury analysis results (GET, department head only)

## Current Limitations

**Technical Limitations:**

The current deployment uses SQLite as the database engine. While suitable for development, SQLite is not appropriate for production environments with concurrent users because it does not handle multiple simultaneous write operations efficiently and lacks the scalability of enterprise databases such as PostgreSQL or MySQL.

The system does not currently send real-time email or SMS notifications to students when invitations are dispatched or when their registration status changes. Students must log in to view updates.

The system lacks WebSocket support or similar real-time communication technology. Updates require page refresh, which may delay awareness of time-sensitive competition deadlines.

The HTMX library for partial page updates is listed as optional and not fully implemented, meaning some interactions trigger full page reloads.

The system uses Django's default session-based authentication rather than token-based authentication (JWT), which limits the potential for a mobile application API in the future.

**Functional Limitations:**

The system is designed exclusively for the Department of Computer Science at Kasdi Merbah University. There is no multi-tenancy support to serve multiple departments or universities simultaneously.

While students can upload their academic schedule as a file, the system does not provide tools for professors to directly access or annotate these schedules.

The Gemini API performs best with French and English medical terminology, which are standard in Algerian medical documents. Arabic input may produce less accurate or incomplete structured responses, as the model's training data is predominantly English-centric. This reduces the reliability of AI analysis for students who describe their injuries primarily in Arabic.

The AI features are dependent on a valid Google Gemini API key. Service interruptions or quota limits on the API side will disable the AI analysis features entirely.

## Challenges Overcome During Development

**Role-Based Access Control Design:** Designing a coherent RBAC system across four distinct user types required careful planning of the Django authentication system. Extending Django's AbstractUser model to include a custom role field while maintaining compatibility with the built-in authentication framework presented early design challenges. Ensuring that URL-level access control was consistently enforced across all views required rigorous testing.

**Automated Account Creation:** One of the most delicate technical decisions was the automatic creation of student user accounts upon approval. When the Service Manager approves a student registration, the system must atomically create both the Student record update and the corresponding User account with the student's registration number as both username and default password. Ensuring this operation is idempotent (safe to retry without creating duplicates) required careful design and proper exception handling.

**Absence Record Integrity:** Automatically generating Absence records when a student accepts a participation invitation required careful design to handle edge cases such as a student being invited to the same competition twice, or an absence record already existing from a previous partial workflow.

**AI Integration and Prompt Engineering:** Integrating the Google Gemini API required significant effort in prompt engineering to ensure the model returns strictly structured JSON output without additional commentary, markdown formatting, or preamble text. The system includes post-processing logic to strip any markdown code fences before parsing the JSON response, and error handling for cases where the model returns unexpected output formats.

**CSRF Protection for Public Endpoints:** The competition submission form is publicly accessible without authentication. Balancing security (CSRF protection) with accessibility for external official entities required careful use of CSRF exemption on specific endpoints while maintaining CSRF enforcement on all authenticated routes.

## Future Enhancements

**Database Migration to PostgreSQL:** Transitioning from SQLite to PostgreSQL would enable the system to support concurrent users, handle large datasets efficiently, and provide advanced indexing and full-text search capabilities. This migration is a prerequisite for any production deployment.

**Email and Push Notification System:** Implementing an automated email notification system using Django's email framework (integrated with SMTP or SendGrid) would allow students and staff to receive real-time alerts for invitation dispatch, approval status changes, competition deadlines, and return confirmation reminders.

**Mobile Application:** Developing a companion mobile application for iOS and Android using React Native or Flutter frontend, backed by a Django REST Framework API, would significantly improve accessibility for students who primarily use mobile devices. Push notifications would further enhance time-sensitive communication.

**Multi-Department and Multi-University Support:** Extending the system to support multiple departments and universities through a multi-tenancy architecture would allow institutional deployment at the national level, potentially serving as a unified platform for the Ministry of Higher Education's sports and cultural programs.

**Advanced AI Analytics Dashboard:** Future AI features could include predictive injury risk scoring (identifying students likely to sustain injuries based on activity type and history), personalized training load recommendations, and natural language querying of absence and competition data using a conversational AI interface.

**Professor Integration Module:** A dedicated interface for professors would allow them to view the list of students who have officially justified absences for each session, mark make-up attendance, and receive automated notifications when a student in their class participates in a competition.

**Real-Time WebSocket Notifications:** Implementing WebSocket support would enable instant updates without page refresh, improving user experience for time-sensitive competition deadlines.

**JWT Authentication:** Moving to token-based authentication would enable better integration with mobile applications and third-party services.

## Conclusion

The Student Athlete Management System (SAMS) successfully digitizes the management of sports and cultural activities at the Department of Computer Science, Kasdi Merbah University – Ouargla. By replacing manual workflows with an integrated web platform, SAMS improves efficiency, transparency, and fairness for all stakeholders.

Students benefit from automated absence justification, digital invitation management, and AI-powered medical document analysis that provides immediate guidance. Administrators gain real-time dashboards and streamlined workflows for competition management. The system demonstrates effective application of Django, role-based access control, and Google Gemini API integration — core competencies of the Artificial Intelligence Engineering program.

Technically, SAMS implements four distinct user roles with tailored dashboards, automated absence tracking, and intelligent medical file analysis. The platform handles the complete lifecycle of student participation: from registration and competition invitations to return confirmation and injury reporting.

While limitations exist including SQLite dependency and lack of real-time notifications, they provide a clear roadmap for future enhancement.

## Acknowledgments

- Department of Computer Science faculty and staff at Kasdi Merbah University – Ouargla
- Google Gemini API team for AI capabilities
- Django open-source community
- Kasdi Merbah University administration for their support

## Contact

For questions or support regarding the Student Athlete Management System (SAMS), please contact:

**Khaled Rahm**  
Email: khaledrahmawork@gmail.com

---

**© 2025 Kasdi Merbah University – Ouargla. All rights reserved.**
```
