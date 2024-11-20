- Start environment:
python -m venv venv

-> Windows:
venv\Scripts\activate

-> macOS/Linux:
source venv/bin/activate

- download dependencies on requirements.txt

- run FastAPI app:
uvicorn api_setup:app --reload
- Interactive swagger UI to test /process-menu endpoint:
http://127.0.0.1:8000/docs

- gpt stuff:
Test the Endpoint
POST Request:
URL: http://127.0.0.1:8000/process-menu
Body (JSON):
{
  "text": "Appetizers: Spring Rolls, Garlic Bread\nMain Course: Grilled Chicken, Vegetarian Pizza",
  "model": "gpt-4"
}

- Expected Response:

{
  "structured_menu": {
    "menus": [
      {
        "section": "Appetizers",
        "items": ["Spring Rolls", "Garlic Bread"]
      },
      {
        "section": "Main Course",
        "items": ["Grilled Chicken", "Vegetarian Pizza"]
      }
    ]
  }
}

