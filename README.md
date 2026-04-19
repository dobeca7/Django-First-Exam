# Future Football Stars

Future Football Stars is a Django web application for managing football academies, players, scouting reports, and player skill evaluations.

## Tech Stack
- Python 3.14
- Django 6.0.2
- PostgreSQL
- `python-dotenv`
- Celery
- Redis
- WhiteNoise

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
- Predefined admin groups: `Academy Managers`, `Scouts`, and `Analysts`
- Match management and match participation management
- Top players page (filtered by potential)
- Compare players page (2-3 players side by side)
- Custom template tag for player stars based on average report rating
- Two DRF API endpoints
- Custom 404 and 500 pages
- Responsive UI built with Django templates and Bootstrap
- Asynchronous player stat recalculation after scout report changes
- Static files served in production through WhiteNoise


## Prerequisites
- Python installed
- PostgreSQL installed and running
- A PostgreSQL database created
- Redis running locally for Celery tasks

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

4. Collect static files:

```powershell
python manage.py collectstatic --noinput
```

5. Run the server:

```powershell
python manage.py runserver
```

6. Start the Celery worker in a second terminal:

```powershell
celery -A future_stars worker --pool=solo --loglevel=info
```

7. Open in browser:
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

## Running Tests
The project currently includes 26 automated tests across the `accounts`, `academies`, `players`, and `scouting` apps.

Run all implemented tests with:

```powershell
python manage.py test accounts academies players scouting
```

## Asynchronous Task Processing
The project uses `Celery` with `Redis` for asynchronous background processing.

When a scout report is created, edited, or deleted, a Celery task recalculates and stores:
- the player's average scout report rating
- the total number of scout reports for that player

The task is executed by the Celery worker and does not block the HTTP request.

## Static and Media Files
Static files are stored in the project's `staticfiles/` directory and collected into `static_root/` during deployment.

Production static file serving is handled by `WhiteNoise`, which serves:
- project static assets
- Django admin static assets
- third-party package static assets

The current project uses static assets, including the home page hero image, but does not currently include uploaded media fields such as `ImageField` or `FileField`.

## Security Notes
The project relies on Django's built-in protections together with server-side access control:
- SQL injection protection through Django ORM queries instead of raw SQL
- XSS protection through Django template auto-escaping
- CSRF protection through `CsrfViewMiddleware` and `{% csrf_token %}` in forms
- parameter tampering protection through owner-filtered querysets, permission checks, and form validation
- sensitive configuration stored in environment variables instead of hardcoded secrets

## Notes for Evaluation
- The application requires PostgreSQL for the database connection.
- The asynchronous task flow requires both Redis and a running Celery worker.
- Static files require `collectstatic` before production deployment.
