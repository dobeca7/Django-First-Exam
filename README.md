# Future Football Stars

Future Football Stars is a Django web application for managing football academies, players, scouting reports, match participation, and player evaluation workflows.

## Live Deployment
- Application URL: `http://16.170.194.209/`
- Admin URL: `http://16.170.194.209/admin/`

## Important Usage Notes
- Create an academy first. Players cannot be created until at least one academy exists.
- Create a player before creating scout reports. Scout reports cannot be created until at least one player exists.

## Tech Stack
- Python 3.12+
- Django 6.0.2
- Django REST Framework
- PostgreSQL
- Celery
- Redis
- Nginx
- WhiteNoise
- Docker Compose

## Project Structure
- `future_stars/` - project settings, shared logic, API routing, root URLs
- `accounts/` - custom user model, authentication, profile management
- `academies/` - academy CRUD and owner-specific access rules
- `players/` - player CRUD, top players, compare players, API endpoint
- `matches/` - match management and match participation flows
- `scouting/` - scout reports, skills, async stat recalculation, API endpoint
- `templates/` - shared layout and app templates
- `staticfiles/` - source static assets
- `static_root/` - collected static files for production

## Core Features
- Public section for anonymous visitors
- Private dashboard for authenticated users
- Registration, login, logout, and profile editing
- Extended Django user model with football-specific fields and role-based groups
- Owner-managed CRUD for academies, players, and scout reports
- Match and participation tracking between academies
- Top players page and compare players page
- Two REST API endpoints
- Custom 404 and 500 pages
- Custom template tag for player rating stars
- Async player stat updates with Celery after scout report create, edit, or delete

## Requirements
- Python 3.12 or newer
- PostgreSQL
- Redis
- Pip

## Environment Variables
Create a `.env` file in the project root. You can copy the template:

```powershell
Copy-Item .envtemplate .env
```

Minimal local `.env`:

```env
SECRET_KEY=replace-with-your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1,http://localhost
DB_NAME=future_stars
DB_PASS=replace-with-your-db-password
DB_USER=replace-with-your-db-user
DB_HOST=127.0.0.1
DB_PORT=5432
DEBUG=True
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
```

Notes:
- `SECRET_KEY` is required.
- Local PostgreSQL and Redis must be running.
- For Docker Compose deployment, the same variable names are used.

## Recommended Setup
The recommended way to run the project is Docker Compose. It starts Django, PostgreSQL, Redis, Celery, and Nginx together and is the closest match to the deployed environment.

1. Copy the environment template if needed:

```powershell
Copy-Item .envtemplate .env
```

2. Build and start the containers:

```powershell
docker compose up -d --build
```

3. Apply migrations:

```powershell
docker compose exec web python manage.py migrate
```

4. Collect static files:

```powershell
docker compose exec web python manage.py collectstatic --noinput
```

5. Create a superuser if needed:

```powershell
docker compose exec web python manage.py createsuperuser
```

6. Open:
- `http://127.0.0.1/`
- `http://127.0.0.1/admin/`

7. Stop the stack:

```powershell
docker compose down
```

Important:
- `docker-compose.yml` uses environment variables with safe local defaults.
- For real deployment, set `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and database credentials explicitly.

## Manual Local Setup
Use this setup only if you prefer running PostgreSQL, Redis, Django, and Celery manually outside Docker.

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create the PostgreSQL database:

```sql
CREATE DATABASE future_stars;
```

4. Apply migrations:

```powershell
python manage.py migrate
```

5. Collect static files:

```powershell
python manage.py collectstatic --noinput
```

6. Start the Django development server:

```powershell
python manage.py runserver
```

7. Start Celery in a second terminal:

```powershell
celery -A future_stars worker --pool=solo --loglevel=info
```

8. Open:
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/admin/`

## Optional Admin User

```powershell
python manage.py createsuperuser
```

## API Endpoints
- `GET /api/players/` - public player list API
- `GET /api/reports/` - authenticated scout report list API

## Running Checks

```powershell
python manage.py check
```

## Running Tests
The project includes 20+ automated tests across the custom logic, views, and user-related functionality.

Run the implemented test suites with:

```powershell
python manage.py test accounts academies players scouting
```

## Async Task Processing
The app uses Celery with Redis for asynchronous processing.

When a scout report is created, edited, or deleted, a Celery task recalculates:
- the player's average scout report rating
- the player's total report count

## Static and Media Files
- Static source files live in `staticfiles/`
- Production static files are collected into `static_root/`
- Nginx serves collected static files in the Docker deployment
- WhiteNoise is enabled in Django as an additional production static file layer

The project currently uses static files but does not include uploaded media models such as `ImageField` or `FileField`.

## Deployment Notes
- The deployed version is expected to run on a cloud host with PostgreSQL, Redis, Celery, and Nginx
- If the public host changes, update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`
