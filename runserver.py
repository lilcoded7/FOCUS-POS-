# runserver.py
import os
import sys
from pathlib import Path
from subprocess import call

# ---------------------------
# Handle PyInstaller _MEIPASS for static/templates discovery
# ---------------------------
def resource_path(rel_path: str) -> str:
    base = getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
    return str(Path(base, rel_path))

# ---------------------------
# Set Django settings module
# ---------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")

import django
from django.core.management import call_command

# Initialize Django
django.setup()

# ---------------------------
# Ensure persistent database exists
# ---------------------------
from django.conf import settings

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    user_data_dir = Path.home() / ".my_django_app"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    db_path = user_data_dir / "db.sqlite3"
else:
    db_path = settings.BASE_DIR / "db.sqlite3"

# ---------------------------
# Run migrations
# ---------------------------
try:
    print("Running Django makemigrations...")
    call_command("makemigrations")
    print("Running Django migrate...")
    call_command("migrate")
except Exception as e:
    print(f"Error during migrations: {e}")

# ---------------------------
# Create default superuser if it doesn't exist
# ---------------------------
from django.contrib.auth import get_user_model

User = get_user_model()
SUPERUSER_EMAIL = "admin@gmail.com"
SUPERUSER_PASSWORD = ".the,the,the."

try:
    if not User.objects.filter(email=SUPERUSER_EMAIL).exists():
        print(f"Creating default superuser: {SUPERUSER_EMAIL}")
        User.objects.create_superuser(
            email=SUPERUSER_EMAIL,
            password=SUPERUSER_PASSWORD
        )
    else:
        print(f"Superuser {SUPERUSER_EMAIL} already exists")
except Exception as e:
    print(f"Error creating superuser: {e}")

# ---------------------------
# Kill process using port (Windows)
# ---------------------------
PORT = int(os.getenv("PORT", "8765"))

if sys.platform.startswith("win"):
    import subprocess
    try:
        output = subprocess.check_output(f'netstat -ano | findstr :{PORT}', shell=True).decode()
        for line in output.strip().splitlines():
            pid = int(line.strip().split()[-1])
            subprocess.call(f'taskkill /PID {pid} /F', shell=True)
            print(f"Killed process {pid} using port {PORT}")
    except subprocess.CalledProcessError:
        pass  # no process using the port

# ---------------------------
# Start Waitress server
# ---------------------------
from django.core.wsgi import get_wsgi_application
from waitress import serve

application = get_wsgi_application()

host = "127.0.0.1"
print(f"Starting Django with Waitress at http://{host}:{PORT}")
serve(application, host=host, port=PORT)
