import json
import requests
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PDFUploadForm
from database_handler.models import (
    Restaurant,
    MenuItem,
    Menu,
    ProcessingLog,
    FoodItem,
    FoodItemRestriction,
    DietaryRestriction,
)
from .utils import extract_text_from_pdf
from database_handler.utils import check_mysql_connection, insert_menu_data
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict
from django.conf import settings
from django.core.paginator import Paginator


def get_filtered_items(dietary_filter):
    if dietary_filter:
        return FoodItemRestriction.objects.filter(
            dietary_restriction__name__iexact=dietary_filter
        ).select_related("food_item")
    return FoodItemRestriction.objects.all().select_related("food_item")


@csrf_exempt
def upload_pdf(request):
    """
    View to handle PDF file upload.
    Handles the POST request to upload a PDF file using the `PDFUploadForm`.
    After uploading the file, the text content is extracted from the PDF and processed.
    """
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES["file"]
            extracted_text = extract_text_from_pdf(pdf_file)

            # Render a page to show the extracted text and confirm sending to AI
            return render(
                request,
                "menu/confirm_text.html",
                {"extracted_text": extracted_text},
            )
    else:
        form = PDFUploadForm()

    return render(request, "menu/upload_pdf.html", {"form": form})


@csrf_exempt
def process_text(request):
    if request.method == "POST":
        extracted_text = request.POST.get("extracted_text")
        data = {"text": extracted_text, "model": "gpt-4"}

        # Debug: Print the JSON data before sending it to the FastAPI endpoint
        print("Sending JSON data to FastAPI endpoint:", json.dumps(data, indent=4))

        response = requests.post(settings.FASTAPI_URL, json=data)

        if response.status_code == 200:
            structured_menu = response.json().get("structured_menu")
            print(
                "Received structured menu:", structured_menu
            )  # Debug: Print the received structured menu
            try:
                structured_menu_parsed = json.loads(structured_menu)
                insert_menu_data(structured_menu_parsed)
                return render(
                    request,
                    "menu/pdf_upload_success.html",
                    {"structured_menu": structured_menu_parsed},
                )
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {e}")
                return JsonResponse({"error": "Failed to decode JSON"}, status=500)
        else:
            return JsonResponse(
                {"error": "Failed to process menu"}, status=response.status_code
            )

    return JsonResponse({"error": "Invalid request method"}, status=400)


def home(request):
    db_connection_success = check_mysql_connection()
    total_restaurants = Restaurant.objects.count()
    total_menus = Menu.objects.count()
    recent_restaurants = Restaurant.objects.order_by("-created_at")[:5]

    # Get dietary restrictions filter
    dietary_filter = request.GET.getlist("dietary")

    # Get sort_by_restaurant parameter
    sort_by_restaurant = request.GET.get("sort_by_restaurant") == "true"

    # Filter food items by dietary restrictions
    filtered_items = (
        FoodItemRestriction.objects.filter(
            dietary_restriction__name__in=dietary_filter
        ).select_related("food_item", "food_item__menuitem__menu__restaurant")
        if dietary_filter
        else None
    )

    # Group filtered food items by restaurant if sorting is requested
    grouped_filtered_items = defaultdict(list)
    if filtered_items and sort_by_restaurant:
        for item in filtered_items:
            restaurant = item.food_item.menuitem.menu.restaurant
            grouped_filtered_items[restaurant].append(item.food_item)

    context = {
        "db_connection_success": db_connection_success,
        "total_restaurants": total_restaurants,
        "total_menus": total_menus,
        "recent_restaurants": recent_restaurants,
        "filtered_items": filtered_items if not sort_by_restaurant else None,
        "grouped_filtered_items": (
            grouped_filtered_items if sort_by_restaurant else None
        ),
        "dietary_restrictions": DietaryRestriction.objects.all(),
        "selected_restrictions": dietary_filter,
        "sort_by_restaurant": sort_by_restaurant,
    }
    return render(request, "menu/home.html", context)


def restaurant_list(request):
    """
    View to display the list of restaurants.

    Args:
    - request: The HTTP request object.

    Returns:
    - Rendered HTML page with the list of restaurants.
    """
    restaurants = Restaurant.objects.all()
    paginator = Paginator(restaurants, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "menu/restaurant_list.html", {"page_obj": page_obj})


def restaurant_detail(request, restaurant_id):
    """
    View to display the details of a specific restaurant's menu, including past menus.

    Args:
    - request: The HTTP request object.
    - restaurant_id: The ID of the restaurant to display.

    Returns:
    - Rendered HTML page with the restaurant's menu details.
    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    # Get the active menu
    active_menu = Menu.objects.filter(restaurant=restaurant, is_active=True).first()

    # Get menu items for the active menu
    if active_menu:
        menu_items = (
            MenuItem.objects.filter(menu=active_menu)
            .select_related("menu", "menu_section", "food_item")
            .prefetch_related("food_item__fooditemrestriction_set__dietary_restriction")
        )
        sections = defaultdict(list)
        for item in menu_items:
            sections[item.menu_section.name].append(
                {
                    "food_item": item.food_item.name,
                    "price": float(item.price),
                    "description": item.food_item.description,
                    "dietary_restrictions": [
                        restriction.dietary_restriction.name
                        for restriction in item.food_item.fooditemrestriction_set.all()
                    ],
                }
            )
    else:
        sections = {}

    return render(
        request,
        "menu/restaurant_detail.html",
        {
            "restaurant": restaurant,
            "active_menu": active_menu,
            "sections_json": json.dumps(sections),
        },
    )


def past_menus(request, restaurant_id):
    """
    View to display the past menus of a specific restaurant.
    """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    past_menus = Menu.objects.filter(
        restaurant=restaurant, 
        is_active=False
    ).order_by("-version")
    
    # Get menu items for each past menu
    menu_details = {}
    for menu in past_menus:
        menu_items = (
            MenuItem.objects.filter(menu=menu)
            .select_related("menu", "menu_section", "food_item")
            .prefetch_related("food_item__fooditemrestriction_set__dietary_restriction")
        )
        sections = defaultdict(list)
        for item in menu_items:
            sections[item.menu_section.name].append(
                {
                    "food_item": item.food_item.name,
                    "price": float(item.price),
                    "description": item.food_item.description,
                    "dietary_restrictions": [
                        restriction.dietary_restriction.name
                        for restriction in item.food_item.fooditemrestriction_set.all()
                    ],
                }
            )
        menu_details[menu.id] = json.dumps(sections)

    return render(
        request,
        "menu/past_menus.html",
        {
            "restaurant": restaurant,
            "past_menus": past_menus,
            "menu_details": menu_details,
        },
    )


def filter_menu_items(request):
    dietary_filter = request.GET.get("dietary")
    if dietary_filter:
        filtered_items = FoodItemRestriction.objects.filter(
            dietary_restriction__name__iexact=dietary_filter
        ).select_related("food_item")
    else:
        filtered_items = FoodItemRestriction.objects.all().select_related("food_item")
    dietary_restrictions = DietaryRestriction.objects.all()

    return render(
        request,
        "menu/filtered_menu.html",
        {
            "filtered_items": filtered_items,
            "dietary_restrictions": dietary_restrictions,
        },
    )


def filter_foods(request):
    selected_restrictions = request.GET.getlist("dietary")
    if selected_restrictions:
        filtered_items = FoodItemRestriction.objects.filter(
            dietary_restriction__name__in=selected_restrictions
        ).select_related("food_item", "dietary_restriction")
    else:
        filtered_items = FoodItemRestriction.objects.all().select_related(
            "food_item", "dietary_restriction"
        )
    dietary_restrictions = DietaryRestriction.objects.all()

    return render(
        request,
        "menu/filter_foods.html",
        {
            "filtered_items": filtered_items,
            "dietary_restrictions": dietary_restrictions,
            "selected_restrictions": selected_restrictions,
        },
    )


def reports_home(request):
    """
    View to display the home page for reports.
    """
    return render(request, "menu/reports/reports_home.html")


def menu_report(request):
    """
    View to generate a report on all menus.
    """
    menus = Menu.objects.select_related("restaurant").all().order_by("restaurant__name", "-version")
    context = {"menus": menus}
    return render(request, "menu/reports/menu_report.html", context)


def food_item_restriction_report(request):
    """
    View to generate a report on food item restrictions.
    """
    food_items = FoodItem.objects.prefetch_related(
        "fooditemrestriction_set__dietary_restriction"
    ).all()
    context = {"food_items": food_items}
    return render(request, "menu/reports/food_item_restriction.html", context)


def processing_log_report(request):
    """
    View to generate a report on menu processing logs.
    """
    logs = ProcessingLog.objects.all().order_by("-action_time")
    context = {"logs": logs}
    return render(request, "menu/reports/processing_log_report.html", context)


def active_menu_report(request):
    """
    View to generate a report on active menus.
    """
    active_menus = Menu.objects.filter(is_active=True).select_related("restaurant").order_by("restaurant__name")
    context = {"active_menus": active_menus}
    return render(request, "menu/reports/active_menu_report.html", context)


def menu_detail(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    versions = Menu.objects.filter(restaurant=menu.restaurant).order_by("-version")
    return render(
        request, "menu/menu_detail.html", {"menu": menu, "versions": versions}
    )

def filter_restrictions_by_food(request):
    selected_food = request.GET.get("food")
    if selected_food:
        filtered_restrictions = FoodItemRestriction.objects.filter(
            food_item__name__iexact=selected_food
        ).select_related("dietary_restriction")
    else:
        filtered_restrictions = FoodItemRestriction.objects.all().select_related(
            "food_item", "dietary_restriction"
        )
    food_items = FoodItem.objects.all()

    return render(
        request,
        "menu/filter_restrictions.html",
        {
            "filtered_restrictions": filtered_restrictions,
            "food_items": food_items,
            "selected_food": selected_food,
        },
    )


@csrf_exempt
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
