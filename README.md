```
How to Run the Project Locally
Follow these instructions to set up and run the Parking EAFIT P1 Django application on your local machine.

Prerequisites
Before you begin, ensure you have the following installed on your system:

Python (v3.8 or higher recommended)

pip (Python package installer)

Step-by-Step Instructions

1. Clone the repository and navigate to the project directory
Open your terminal or command prompt and navigate to the folder containing the manage.py file:

cd parking

2. Install Dependencies
Install Django and any other required packages. (Note: If you have a requirements.txt file, use pip install -r requirements.txt instead).

pip install django

3. Apply Database Migrations
Since the project uses an SQLite database (db.sqlite3), ensure all models from the parqueadero app are properly synced:

python manage.py migrate

4. Run the Development Server
Start the local Django server with the following command:

python manage.py runserver

(Optional parameter: You can specify a different port if 8000 is occupied, e.g., python manage.py runserver 8080)

5. Access the Application
Once the server is running, open your preferred web browser and go to:

http://127.0.0.1:8000/


├── 📁 Parking
│   ├── 📁 Config
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 asgi.py
│   │   ├── 🐍 settings.py
│   │   ├── 🐍 urls.py
│   │   └── 🐍 wsgi.py
│   ├── 📁 monitoreo
│   │   ├── 📁 migrations
│   │   │   ├── 🐍 0001_initial.py
│   │   │   └── 🐍 __init__.py
│   │   ├── 📁 static
│   │   │   └── central.png
│   │   │   └── idiomas.png
│   │   │   └── ingenieros.png
│   │   │   └── logo.png
│   │   │   └── styles.css
│   │   ├── 📁 templates
│   │   │   └── 🌐 dashboard.html
│   │   │   └── 🌐 p_central.html
│   │   │   └── 🌐 p_idiomas.html
│   │   │   └── 🌐 p_ingenieros.html
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 admin.py
│   │   ├── 🐍 apps.py
│   │   ├── 🐍 models.py
│   │   ├── 🐍 tests.py
│   │   └── 🐍 views.py
│   ├── 📄 db.sqlite3
└───└── 🐍 manage.py
```
