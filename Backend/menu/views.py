import json
import requests
from django.shortcuts import render, redirect
from .forms import PDFUploadForm
from .models import PDFUpload
from .utils import extract_text_from_pdf
from database_handler.utils import check_mysql_connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_pdf(request):
    """
    View to handle PDF file upload.
    Handles the POST request to upload a PDF file using the `PDFUploadForm`.
    After uploading the file, the text content is extracted from the PDF and saved in the database.
    """
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the uploaded PDF to the database
            pdf_file = form.instance  # Get the saved PDF file instance
            # Extract text from the uploaded PDF
            extracted_text = extract_text_from_pdf(pdf_file.file.path)

            # Render a page to show the extracted text and confirm sending to AI
            return render(
                request,
                "menu/confirm_text.html",
                {"extracted_text": extracted_text, "pdf_id": pdf_file.id},
            )
    else:
        form = PDFUploadForm()

    return render(request, "menu/upload_pdf.html", {"form": form})

@csrf_exempt
def process_text(request):
    """
    View to process the extracted text with the AI.
    """
    if request.method == "POST":
        extracted_text = request.POST.get("extracted_text")
        pdf_id = request.POST.get("pdf_id")

        # Prepare the data for the FastAPI endpoint
        data = {
            "text": extracted_text,
            "model": "gpt-4"  # Optional: specify the model if needed
        }

        # Call the FastAPI endpoint
        response = requests.post("http://localhost:8001/process-menu", json=data)

        if response.status_code == 200:
            structured_menu = response.json().get("structured_menu")

            # Ensure structured_menu is a proper Python object (JSON string needs parsing)
            structured_menu_parsed = json.loads(structured_menu)

            # Render the result, showing the structured menu
            return render(
                request,
                "menu/pdf_upload_success.html",
                {"structured_menu": structured_menu_parsed},
            )
        else:
            return JsonResponse({"error": "Failed to process menu"}, status=response.status_code)

    return JsonResponse({"error": "Invalid request method"}, status=400)

def home(request):
    """
    Home page view.
    """
    db_connection_success = check_mysql_connection()
    return render(
        request, "menu/home.html", {"db_connection_success": db_connection_success}
    )
