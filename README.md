# Django REST API

A Django REST Framework API for user profile management and authentication.

## Requirements

- Python 3.8
- The packages listed in `requirements.txt`

## Installation

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Configure environment variables

The Django secret key is intentionally not stored in this repository. Set a unique key in each environment.

### macOS / Linux

```bash
export DJANGO_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"
export DJANGO_DEBUG=True
export DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

### Windows PowerShell

```powershell
$env:DJANGO_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(50))"
$env:DJANGO_DEBUG = "True"
$env:DJANGO_ALLOWED_HOSTS = "localhost,127.0.0.1"
```

Do not commit real secret keys or local `.env` files. For production, set `DJANGO_DEBUG=False` and configure `DJANGO_ALLOWED_HOSTS` with the exact hostnames serving the application.

## Run the application

Apply migrations first:

```bash
python manage.py migrate
python manage.py runserver
```

## Run regression tests

```bash
python manage.py test profiles_api
```

The profile API regression tests cover authentication, profile list/detail privacy, owner-only updates, and password hashing. GitHub Actions runs this test command for pull requests and pushes to the main development branch.

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss the proposed change.
