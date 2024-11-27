from django.shortcuts import render, redirect
from .forms import PDFUploadForm
from .models import PDFUpload
from .utils import extract_text_from_pdf
from database_handler.utils import check_mysql_connection


def upload_pdf(request):
    """
    View to handle PDF file upload.

    Handles the POST request to upload a PDF file using the `PDFUploadForm`.
    After uploading the file, the text content is extracted from the PDF and saved in the database.

    Args:
    - request: The HTTP request object.

    Returns:
    - Rendered HTML page with form or redirect upon success.
    """
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the uploaded PDF to the database
            pdf_file = form.instance  # Get the saved PDF file instance
            # Extract text from the uploaded PDF
            extracted_text = extract_text_from_pdf(pdf_file.file.path)
            # Render the result, showing the extracted text
            return render(
                request,
                "menu/pdf_upload_success.html",
                {"extracted_text": extracted_text},
            )
    else:
        form = PDFUploadForm()

    return render(request, "menu/upload_pdf.html", {"form": form})


def home(request):
    """
    Home page view.

    The home page is typically the main entry point for the web application.
    It may render the main landing page or provide navigation to other sections of the site.

    Args:
    - request: The HTTP request object.

    Returns:
    - Rendered HTML page for the homepage.
    """
    db_connection_success = check_mysql_connection()
    return render(
        request, "menu/home.html", {"db_connection_success": db_connection_success}
    )
