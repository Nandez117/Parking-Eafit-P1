# Parking EAFIT - Estimated Waiting Time

## User Story

**US-08**

**As a** parking lot user  
**I want** to know the estimated waiting time in the entry queue  
**So that** I can make informed decisions before entering the campus.

### Acceptance Criteria

- The system estimates the waiting time based on vehicular flow.  
- The information is displayed clearly to the user.  
- The estimation helps the user decide whether to enter the campus or not.

---

## Project Description

This web application allows users to view the **estimated waiting time** at EAFIT campus parking lots.  
It is built using **Django**, and the frontend includes:

- Display of parking lots with representative images.  
- Display of estimated waiting time in minutes.  
- Dynamic color coding to indicate low (green) or high (red) waiting times.  

---

## Autor

Isabella Cadavid Posada

---

## Requirements

- Python 3.x  
- Django 4.x or higher  
- Modern web browser (Chrome, Firefox, Edge)

---

## How to Run the Project

1. Clone the repository and switch to the `IsaC` branch:

```bash
git clone -b IsaC https://github.com/Nandez117/timeparkingproject.git
Navigate to the project folder:

cd timeparkingproject
(Optional but recommended) Create a virtual environment:

python -m venv venv
Activate the virtual environment:

Windows:

venv\Scripts\activate
Linux / Mac:

source venv/bin/activate
Install dependencies:

pip install django
Run database migrations:

python manage.py migrate
Start the local server:

python manage.py runserver
Open a web browser and go to:

http://127.0.0.1:8000/
