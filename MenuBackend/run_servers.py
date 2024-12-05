import sys
import subprocess
from pathlib import Path

# Get the path to the virtual environment's Python
VENV_PYTHON = sys.executable

def run_servers():
    django_command = [VENV_PYTHON, "manage.py", "runserver"]
    fastapi_command = [VENV_PYTHON, "-m", "uvicorn", "FastApiApp.api_setup:app", "--reload", "--port", "8001"]
    
    django_process = subprocess.Popen(django_command)
    fastapi_process = subprocess.Popen(fastapi_command)
    
    try:
        django_process.wait()
        fastapi_process.wait()
    except KeyboardInterrupt:
        django_process.terminate()
        fastapi_process.terminate()

if __name__ == "__main__":
    run_servers()
