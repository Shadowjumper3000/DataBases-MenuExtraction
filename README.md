# Restaurant Menu Manager

## Features
- Upload PDF menus and extract text
- Process extracted text using OpenAI's GPT-4 model
- Display structured menu data

## Installation

### 1. Create a virtual environment:
- For Windows
    ```sh
    python -m venv venv
    ```
- For Linux/macOS
    ```sh
    python3 -m venv venv
    ```

### 2. Activate the virtual environment:
- For Windows
    ```sh
    .\venv\Scripts\activate
    ```
- For Linux/macOS
    ```sh
    source venv/bin/activate
    ```

### 3. Install the required dependencies:
- For Windows
    ```sh
    pip install -r requirements.txt
    ```
- For Linux/macOS
    ```sh
    pip3 install -r requirements.txt
    ```

### 4. Modify Django settings to use the new database:
- Open `settings.py` in your Django project.
- Update the `DATABASES` setting to use the new database:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'restaurants',
            'USER': 'your_username',  # Change this
            'PASSWORD': 'your_password',  # Change this
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
    ```

### 5. Apply the migrations:
- For Windows
    ```sh
    python manage.py makemigrations database_handler
    python manage.py migrate
    ```
- For Linux/macOS
    ```sh
    python3 manage.py makemigrations database_handler
    python3 manage.py migrate
    ```

### 6. Create a superuser:
- For Windows
    ```sh
    python manage.py createsuperuser
    ```
- For Linux/macOS
    ```sh
    python3 manage.py createsuperuser
    ```

### 7. Set the OpenAI API key:
- Create a `.env` file in the FastApiApp directory of the project.
- Add the following line to the `.env` file:
    ```sh
    OPENAI_API_KEY=<your_api_key>
    ```

### 8. Run the Django and the FastAPI servers:
- For Windows
    ```sh
    python run_servers.py
    ```
- For Linux/macOS
    ```sh
    python3 run_servers.py
    ```
### 9. Access the application:
- Open your web browser and go to `http://127.0.0.1:8000/` for the Django application.
- The FastAPI server will be running on `http://127.0.0.1:8001/`.

## Notes
- The Django application handles the PDF upload and text extraction.
- The FastAPI application processes the extracted text using OpenAI's GPT-4 model.
- The database is created automatically on the host machine, so mysql must be installed and running.