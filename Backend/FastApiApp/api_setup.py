import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
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
    # Ensure API key is available
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not found.")

    # Validate input text
    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    # Generate a structured prompt for the model
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
        '  "menus": [\n'
        "    {\n"
        '      \"section\": \"Appetizers\",  # Example section\n'
        '      \"items\": [\n'
        '        \"Spring Rolls\",\n'
        '        \"Garlic Bread\"\n'
        '      ]\n'
        "    },\n"
        "    {\n"
        '      \"section\": \"Main Course\",\n'
        '      \"items\": [\n'
        '        \"Grilled Salmon\",\n'
        '        \"Steak\"\n'
        '      ]\n'
        "    }\n"
        "  ]\n"
        "}"
    )

    try:
        # Corrected API call using openai.chat.completions.create()
        response = openai.chat.completions.create(
            model=input_data.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that processes menu data."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3,  # Keep responses deterministic for structured tasks
        )

        # Correct access pattern to get the content of the message
        structured_menu = response.choices[0].message.content.strip()

        return {"structured_menu": structured_menu}

    except openai.OpenAIError as exc:
        raise HTTPException(status_code=400, detail=f"OpenAI API error: {str(exc)}") from exc