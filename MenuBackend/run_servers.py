import subprocess
import os
import sys

def run_django_server():
    # Run the Django server by calling manage.py directly from MenuBackend
    subprocess.run([sys.executable, "manage.py", "runserver"])

def run_fastapi_server():
    # Run the FastAPI server by calling uvicorn from the FastApiApp folder
    subprocess.run(["uvicorn", "FastApiApp.api_setup:app", "--host", "0.0.0.0", "--port", "8001", "--reload"])

def run_servers():
    # Run Django and FastAPI servers in parallel
    django_process = subprocess.Popen([sys.executable, "manage.py", "runserver"])
    fastapi_process = subprocess.Popen(["uvicorn", "FastApiApp.api_setup:app", "--host", "0.0.0.0", "--port", "8001", "--reload"])

    try:
        django_process.wait()
        fastapi_process.wait()
    except KeyboardInterrupt:
        print("Terminating both servers...")
        django_process.terminate()
        fastapi_process.terminate()

if __name__ == "__main__":
    run_servers()
