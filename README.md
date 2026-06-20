#"this is caresync project"
https://caresync-hospital-management-system-2.onrender.com





```mermaid
flowchart TB

%% Layer 1
subgraph L1["👥 User Layer"]
    Patient["Patient"]
    Admin["Admin"]
    Staff["Hospital Staff"]
end

%% Layer 2
subgraph L2["🌐 Presentation Layer"]
    Frontend["HTML + CSS + Bootstrap + JavaScript + Jinja2"]
end

%% Layer 3
subgraph L3["🔐 Authentication & Security Layer"]
    Login["Login / Registration"]
    OTP["OTP Verification"]
    Session["Session Management"]
    Reset["Password Recovery"]
end

%% Layer 4
subgraph L4["⚙️ Application Layer (Flask Backend)"]
    PatientModule["Patient Management"]
    AppointmentModule["Appointment Management"]
    FaceModule["Face Recognition Module"]
    AdminModule["Admin Dashboard"]
    NotificationModule["Email Notification Service"]
end

%% Layer 5
subgraph L5["🤖 AI Face Recognition Layer"]
    Capture["Face Capture"]
    Detection["Face Detection"]
    Encoding["Face Encoding"]
    Matching["Face Verification"]
end

%% Layer 6
subgraph L6["🗄️ Data Layer"]
    PatientDB["Patient Records"]
    AppointmentDB["Appointments"]
    FaceDB["Face Embeddings"]
    AdminDB["Admin Data"]
end

%% Layer 7
subgraph L7["☁️ External Services Layer"]
    Cloudinary["Cloudinary Image Storage"]
    Email["SMTP / Email Service"]
end

Patient --> Frontend
Admin --> Frontend
Staff --> Frontend

Frontend --> Login
Frontend --> OTP
Frontend --> Session
Frontend --> Reset

Login --> PatientModule
Login --> AppointmentModule
Login --> FaceModule
Login --> AdminModule

FaceModule --> Capture
Capture --> Detection
Detection --> Encoding
Encoding --> Matching

PatientModule --> PatientDB
AppointmentModule --> AppointmentDB
AdminModule --> AdminDB
Matching --> FaceDB

FaceModule --> Cloudinary
NotificationModule --> Email

AppointmentModule --> NotificationModule
PatientModule --> NotificationModule
```

```mermaid
flowchart TD

%% Layer 1
subgraph L1["👥 User Layer"]
    Patient["Patient"]
    Admin["Admin"]
    Staff["Hospital Staff"]
end

%% Layer 2
subgraph L2["🌐 Presentation Layer"]
    Web["Web Interface"]
    UI["HTML • CSS • Bootstrap • JavaScript • Jinja2"]
end

%% Layer 3
subgraph L3["🔐 Authentication Layer"]
    Login["Login"]
    Register["Registration"]
    OTP["OTP Verification"]
    Reset["Password Reset"]
    Session["Session Management"]
end

%% Layer 4
subgraph L4["🤖 Face Recognition Layer"]
    Capture["Face Capture"]
    Detect["Face Detection"]
    Extract["Feature Extraction"]
    Encode["Face Embedding"]
    Match["Face Matching"]
    Verify["Identity Verification"]
end

%% Layer 5
subgraph L5["🏥 Business Logic Layer"]
    PatientMgmt["Patient Management"]
    AppointmentMgmt["Appointment Management"]
    AdminMgmt["Admin Management"]
    NotificationMgmt["Notification Management"]
end

%% Layer 6
subgraph L6["⚙️ Service Layer"]
    AuthService["Authentication Service"]
    PatientService["Patient Service"]
    AppointmentService["Appointment Service"]
    FaceService["Face Recognition Service"]
    AdminService["Admin Service"]
    EmailService["Email Service"]
end

%% Layer 7
subgraph L7["🗃️ Data Access Layer"]
    ORM["SQLAlchemy ORM"]
    DBOps["Database Operations"]
end

%% Layer 8
subgraph L8["🛢️ Database Layer"]
    PatientDB["Patient Database"]
    AppointmentDB["Appointment Database"]
    FaceDB["Face Embeddings"]
    AdminDB["Admin Database"]
    Logs["Audit Logs"]
end

%% Layer 9
subgraph L9["☁️ External Services Layer"]
    Cloudinary["Cloudinary Storage"]
    SMTP["Email Service"]
    OTPService["OTP Service"]
end

%% Connections
Patient --> Web
Admin --> Web
Staff --> Web

Web --> UI
UI --> Login
UI --> Register

Login --> OTP
Register --> OTP
OTP --> Session

Session --> Capture

Capture --> Detect
Detect --> Extract
Extract --> Encode
Encode --> Match
Match --> Verify

Verify --> PatientMgmt
Verify --> AppointmentMgmt
Verify --> AdminMgmt

PatientMgmt --> PatientService
AppointmentMgmt --> AppointmentService
AdminMgmt --> AdminService
NotificationMgmt --> EmailService

AuthService --> ORM
PatientService --> ORM
AppointmentService --> ORM
FaceService --> ORM
AdminService --> ORM

ORM --> DBOps

DBOps --> PatientDB
DBOps --> AppointmentDB
DBOps --> FaceDB
DBOps --> AdminDB
DBOps --> Logs

FaceService --> Cloudinary
EmailService --> SMTP
AuthService --> OTPService
```


| Layer                | Technology                               |
| -------------------- | ---------------------------------------- |
| User Layer           | Patient, Admin, Hospital Staff           |
| Presentation Layer   | HTML, CSS, Bootstrap, JavaScript, Jinja2 |
| Authentication Layer | Flask Sessions, OTP, Password Recovery   |
| Application Layer    | Python, Flask, Blueprints                |
| AI Layer             | OpenCV, face_recognition, NumPy          |
| Data Layer           | SQLite / PostgreSQL, SQLAlchemy          |
| External Services    | Cloudinary, SMTP Email Service           |
| Deployment Layer     | Render, Gunicorn                         |
