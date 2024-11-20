from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define input model
class TextInput(BaseModel):
    text: str
    model: str = "gpt-4"  # Default to GPT-4, can be changed to gpt-3.5-turbo

# Placeholder function for formatting the prompt
def generate_prompt(text: str) -> str:
    return (
        "You are an AI assistant that processes restaurant menu text. The text provided is extracted "
        "from a PDF and may not have perfect formatting. Your job is to structure this text into a "
        "JSON format. Group menu items under appropriate sections (e.g., Appetizers, Main Course, Drinks). "
        "If no clear section is identified, create an 'Uncategorized' section.\n\n"
        f"Input Text:\n{text}\n\n"
        "Output JSON Format:\n"
        "{\n"
        "  \"menus\": [\n"
        "    {\n"
        "      \"section\": \"Section Name\",\n"
        "      \"items\": [\"Item 1\", \"Item 2\"]\n"
        "    },\n"
        "    ...\n"
        "  ]\n"
        "}"
    )

# API endpoint
@app.post("/process-menu")
async def process_menu(input_data: TextInput):
    logger.info("Received text for processing.")

    # Validate input
    if len(input_data.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    # Generate the prompt
    prompt = generate_prompt(input_data.text)

    try:
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model=input_data.model,  # Use GPT-4 or GPT-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3  # Keep responses deterministic for structured tasks
        )

        # Extract the generated response
        structured_output = response.choices[0].message["content"]
        logger.info("Response successfully generated.")
        return {"structured_menu": structured_output}

    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"OpenAI API error: {str(e)}")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
