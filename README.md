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
