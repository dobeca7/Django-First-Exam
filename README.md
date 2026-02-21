# Future Football Stars (Django Project)

Web application for managing football academies, young players, scouting reports, and skills.

## Tech Stack
- Python 3.14
- Django 6.0.2
- PostgreSQL
- python-dotenv

## Project Structure
- `future_stars/` - Django project settings and URLs
- `academies/` - academy domain logic
- `players/` - player domain logic
- `scouting/` - skills and scout reports
- `templates/` - global templates

## Prerequisites
- Python installed
- PostgreSQL installed and running
- A PostgreSQL database created (example: `future_stars`)

## Environment Variables
Copy from `.envtemplate


## Installation and Run
1. Create virtual environment and activate it:
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:
```powershell
pip install django psycopg2-binary python-dotenv
```

3. Make and apply migrations:
```powershell
python manage.py makemigrations
python manage.py migrate
```

4. Run development server:
```powershell
python manage.py runserver
```

5. Open:
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/admin/`

## Optional Admin User
```powershell
python manage.py createsuperuser
```
