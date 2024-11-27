# Restaurant Menu Manager

## Features

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

### 4. Run `schema.sql` to create the database:
- Ensure you have MySQL installed and running.
- Execute the `schema.sql` file to create the database and tables:
    ```sh
    mysql -u your_username -p your_password < schema.sql
    ```

### 5. Modify Django settings to use the new database:
- Open `settings.py` in your Django project.
- Update the `DATABASES` setting to use the new database:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'restaurants',
            'USER': 'your_username',
            'PASSWORD': 'your_password',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
    ```

### 6. Apply the migrations:
- For Windows
    ```sh
    python manage.py migrate
    ```
- For Linux/macOS
    ```sh
    python3 manage.py migrate
    ```

### 7. Create a superuser:
- For Windows
    ```sh
    python manage.py createsuperuser
    ```
- For Linux/macOS
    ```sh
    python3 manage.py createsuperuser
    ```

### 8. Run the development server:
- For Windows
    ```sh
    python manage.py runserver
    ```
- For Linux/macOS
    ```sh
    python3 manage.py runserver
    ```

### 9. Access the application:
Open your web browser and go to `http://127.0.0.1:8000/` or `http://127.0.0.1:8000/admin` for the admin interface.