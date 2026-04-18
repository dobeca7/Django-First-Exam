# Future Football Stars

Future Football Stars is a Django web application for managing football academies, players, scouting reports, and player skill evaluations.

## Tech Stack
- Python 3.14
- Django 6.0.2
- PostgreSQL
- `python-dotenv`
- Celery
- Redis

## Project Structure
- `future_stars/` - project settings, root URLs, shared project-level code
- `academies/` - academy CRUD and related business logic
- `players/` - player CRUD, top players, player comparison
- `scouting/` - scout reports and skills
- `templates/` - shared and app templates
- `staticfiles/` - project static assets (images, etc.)

## Features
- Public football data section for anonymous visitors
- Private account dashboard for authenticated users
- User registration, login, logout, and profile editing
- Extended custom user model with football-related profile fields
- Predefined admin groups: `Academy Managers` and `Scouts`
- Top players page (filtered by potential)
- Compare players page (2-3 players side by side)
- Custom template tag for player stars based on average report rating


## Prerequisites
- Python installed
- PostgreSQL installed and running
- A PostgreSQL database created

## Environment Variables
Create a `.env` file in the project root. You can copy `.envtemplate` and fill values:

```powershell
Copy-Item .envtemplate .env
```

Required variables:

```env
SECRET_KEY=your-django-secret-key
DB_NAME=future_stars
DB_PASS=your_db_password
DB_USER=your_db_user
DB_HOST=127.0.0.1
DB_PORT=5432
DEBUG=False
ALLOWED_HOSTS=127.0.0.1,localhost
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
```

Notes:
- `SECRET_KEY` must be set.
- Database settings must match your local PostgreSQL instance.
- Redis must be running locally for Celery background tasks.


## PostgreSQL Quick Setup (Example)
If you need a sample local DB setup:

```sql
CREATE DATABASE future_stars;
```

Then make sure `DB_NAME`, `DB_USER`, and `DB_PASS` in `.env` match your PostgreSQL credentials.

## Installation and Run
1. Create and activate virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Apply migrations:

```powershell
python manage.py migrate
```

4. Run the server:

```powershell
python manage.py runserver
```

5. Start the Celery worker in a second terminal:

```powershell
celery -A future_stars worker --pool=solo --loglevel=info
```

6. Open in browser:
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/admin/`

## Optional Admin User
```powershell
python manage.py createsuperuser
```

## Running Checks
```powershell
python manage.py check
```

## Asynchronous Task Processing
The project uses `Celery` with `Redis` for asynchronous background processing.

When a new scout report is created, a Celery task recalculates and stores:
- the player's average scout report rating
- the total number of scout reports for that player

The task is executed by the Celery worker and does not block the HTTP request.
