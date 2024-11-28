from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()


# Define input schema
class TextInput(BaseModel):
    text: str
    model: str = "gpt-4"  # Default model


# Define API endpoint
@app.post("/process-menu")
async def process_menu(input_data: TextInput):
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not found.")

    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    # Generate a structured prompt
    prompt = (
        "You are an AI assistant that processes restaurant menu text. The text provided is extracted "
        "from a PDF and may not have perfect formatting. Your job is to structure this text into a "
        "JSON format. Group menu items under appropriate sections (e.g., Appetizers, Main Course, Drinks). "
        "If no clear section is identified, create an 'Uncategorized' section.\n\n"
        f"Input Text:\n{input_data.text}\n\n"
        "Output JSON Format:\n"
        "{\n"
        '  "restaurant": {\n'
        '    "name": "Restaurant Name",\n'
        '    "address": "Restaurant Address",\n'
        '    "phone_number": "Restaurant Phone Number",\n'
        '    "email": "Restaurant Email",\n'
        '    "website": "Restaurant Website"\n'
        "  },\n"
        '  "menus": [\n'
        "    {\n"
        '      "section": "Section Name",\n'
        '      "items": [\n'
        "        {\n"
        '          "name": "Item Name",\n'
        '          "description": "Item Description",\n'
        '          "price": Item Price,\n'
        '          "allergens": ["Allergen 1", "Allergen 2"],\n'
        '          "dietary_restrictions": ["Vegetarian", "Gluten-Free"]\n'
        "        }\n"
        "      ]\n"
        "    }\n"
        "  ]\n"
        "}\n"
    )

    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model=input_data.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            temperature=0.3,  # Keep responses deterministic for structured tasks
        )
        return {"structured_menu": response.choices[0].message["content"]}
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=400, detail=f"OpenAI API error: {str(e)}")
