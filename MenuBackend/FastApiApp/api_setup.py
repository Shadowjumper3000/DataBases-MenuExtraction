import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import openai

load_dotenv(dotenv_path="FastApiApp/.env")

openai.api_key = os.getenv("OPEN_API_KEY")
app = FastAPI()


class TextInput(BaseModel):
    """
    Input schema for the /process-menu endpoint.
    """

    text: str
    model: str = "gpt-4"  # Default model


@app.post("/process-menu")
async def process_menu(input_data: TextInput):
    """
    Process the menu text and return a structured JSON format.

    Args:
        input_data (TextInput): The input text and model information.

    Returns:
        dict: The structured menu in JSON format.
    """
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not found.")

    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    # Generate a structured prompt for the model
    prompt = (
        "You are an AI assistant that processes restaurant menu text. The text provided is extracted "
        "from a PDF and may not have perfect formatting. Your job is to structure this text into a "
        "JSON format. Each section should be identified, and the menu items under each section should be listed. "
        "If no clear section is identified, create an 'Uncategorized' section and group items under it. "
        "Output the structured JSON format as shown below:\n\n"
        f"Extracted Text:\n{input_data.text}\n\n"
        "Output JSON format:\n"
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
        response = openai.chat.completions.create(
            model=input_data.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that processes menu data.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=5000,
            temperature=0.3,
        )

        structured_menu = response.choices[0].message.content.strip()
        return {"structured_menu": structured_menu}

    except openai.OpenAIError as exc:
        raise HTTPException(
            status_code=400, detail=f"OpenAI API error: {str(exc)}"
        ) from exc
