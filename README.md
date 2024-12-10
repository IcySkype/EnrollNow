# **Web-Based Subject Pre-Registration and Advising System**

## **Overview**
This is a Django-based web application designed to facilitate subject pre-registration and advising for students, instructors, and administrators. The system streamlines course management, subject enrollment, and consultation appointments, with role-based access control for different types of users.
---
## **Features**
- **Authentication & Authorization**
  - Role-based access for students, instructors, and admins.
  - Custom login and logout functionality.

- **Course Management**
  - Manage subject offerings, schedules, and instructors.

- **Subject Enrollment**
  - Students can view and enroll in subjects based on their year level and program.
  - Admins can approve or manage student enrollment.

- **Consultation Appointment**
  - Students can schedule consultations with instructors.
  - Instructors can manage their consultation schedules.
---
## **Technologies Used**
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (default)
- **PDF Generation:** pdfkit with wkhtmltopdf
---

## **Installation**
Follow these steps to get the project up and running on your local machine.
### **1. Clone the Repository**
### **2. Set Up a Virtual Environment**
### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Install wkhtmltopdf**
This project uses `pdfkit` for generating PDFs, which requires `wkhtmltopdf`. Download and install it from [wkhtmltopdf.org](https://wkhtmltopdf.org/).

Ensure it is accessible in your system's PATH.

### **5. Configure the Database**
The default database is SQLite. No additional configuration is required unless you plan to use another database.

Run migrations:
```bash
python manage.py migrate
```

### **6. Create a Superuser**
```bash
python manage.py createsuperuser
```

### **7. Run the Server**
```bash
python manage.py runserver
```

Access the app at `http://127.0.0.1:8000/`.
