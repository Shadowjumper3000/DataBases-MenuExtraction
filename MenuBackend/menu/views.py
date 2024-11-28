from django.shortcuts import render, redirect, get_object_or_404
from .forms import PDFUploadForm
from .models import PDFUpload
from database_handler.models import Restaurant, Menu, MenuSection, MenuItem
from .utils import extract_text_from_pdf
from database_handler.utils import insert_menu_data, check_mysql_connection
from collections import defaultdict
import json


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
    restaurants = Restaurant.objects.all().prefetch_related(
        "menu_set__menusection_set__menuitem_set"
    )
    return render(
        request,
        "menu/home.html",
        {
            "db_connection_success": db_connection_success,
            "restaurants": restaurants,
        },
    )


def restaurant_list(request):
    """
    View to display the list of restaurants.

    Args:
    - request: The HTTP request object.

    Returns:
    - Rendered HTML page with the list of restaurants.
    """
    restaurants = Restaurant.objects.all()
    return render(request, "menu/restaurant_list.html", {"restaurants": restaurants})


def restaurant_detail(request, restaurant_id):
    """
    View to display the details of a specific restaurant's menu.

    Args:
    - request: The HTTP request object.
    - restaurant_id: The ID of the restaurant to display.

    Returns:
    - Rendered HTML page with the restaurant's menu details.
    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = (
        MenuItem.objects.filter(menu__restaurant=restaurant)
        .select_related("menu", "menu_section", "food_item")
        .prefetch_related("food_item__fooditemrestriction_set__dietary_restriction")
    )

    # Group menu items by their sections
    sections = defaultdict(list)
    for item in menu_items:
        sections[item.menu_section].append(item)

    return render(
        request,
        "menu/restaurant_detail.html",
        {"restaurant": restaurant, "sections": sections},
    )


def upload_json(request):
    """
    View to handle JSON data input.

    Handles the POST request to input JSON data and insert it into the database.

    Args:
    - request: The HTTP request object.

    Returns:
    - Redirects to the home page upon success or failure.
    """
    if request.method == "POST":
        json_data = request.POST.get("json_data")
        if json_data:
            try:
                menu_data = json.loads(json_data)
                insert_menu_data(menu_data)
                print("JSON data successfully inserted into the database.")
            except json.JSONDecodeError as e:
                print(f"Invalid JSON data: {e}")
            except Exception as e:
                print(f"Error inserting JSON data into the database: {e}")
        return redirect("home")
    return render(request, "menu/upload_json.html")
