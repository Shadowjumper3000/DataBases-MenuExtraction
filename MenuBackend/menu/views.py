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
from django.core.paginator import Paginator
from collections import defaultdict
from django.conf import settings


def get_filtered_items(dietary_filter):
    if dietary_filter:
        return FoodItemRestriction.objects.filter(
            dietary_restriction__name__iexact=dietary_filter
        ).select_related("food_item")
    return FoodItemRestriction.objects.all().select_related("food_item")


@csrf_exempt
def upload_pdf(request):
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES["file"]
            extracted_text = extract_text_from_pdf(pdf_file)
            return render(
                request, "menu/confirm_text.html", {"extracted_text": extracted_text}
            )
    else:
        form = PDFUploadForm()
    return render(request, "menu/upload_pdf.html", {"form": form})


@csrf_exempt
def process_text(request):
    if request.method == "POST":
        extracted_text = request.POST.get("extracted_text")
        data = {"text": extracted_text, "model": "gpt-4"}
        response = requests.post(settings.FASTAPI_URL, json=data)

        if response.status_code == 200:
            structured_menu = response.json().get("structured_menu")
            structured_menu_parsed = json.loads(structured_menu)
            insert_menu_data(structured_menu_parsed)
            return render(
                request,
                "menu/pdf_upload_success.html",
                {"structured_menu": structured_menu_parsed},
            )
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
    dietary_filter = request.GET.get("dietary")
    filtered_items = get_filtered_items(dietary_filter)
    dietary_restrictions = DietaryRestriction.objects.all()

    context = {
        "db_connection_success": db_connection_success,
        "total_restaurants": total_restaurants,
        "total_menus": total_menus,
        "recent_restaurants": recent_restaurants,
        "filtered_items": filtered_items,
        "dietary_restrictions": dietary_restrictions,
    }
    return render(request, "menu/home.html", context)


def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    paginator = Paginator(restaurants, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "menu/restaurant_list.html", {"page_obj": page_obj})


def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = (
        MenuItem.objects.filter(menu__restaurant=restaurant)
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
    return render(
        request,
        "menu/restaurant_detail.html",
        {"restaurant": restaurant, "sections_json": json.dumps(sections)},
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


def filter_foods_by_restrictions(request):
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
                print(f"Error inserting JSON data: {e}")
        return redirect("home")
    return render(request, "menu/upload_json.html")

def reports_home(request):
    return render(request, "menu/reports_home.html")
