from .models import (
    Restaurant,
    Menu,
    MenuSection,
    MenuItem,
    FoodItem,
    DietaryRestriction,
    FoodItemRestriction,
    ProcessingLog,
)
from django.conf import settings
import MySQLdb
import json
from decimal import Decimal, InvalidOperation


def insert_menu_data(menu_data):
    """
    Insert structured menu data into database.

    Args:
        menu_data (dict): Structured menu data containing restaurant and menu information

    Returns:
        None
    """
    print("Inserting menu data:", menu_data)

    # Insert restaurant data
    restaurant_data = menu_data["restaurant"]
    restaurant, created = Restaurant.objects.get_or_create(
        name=restaurant_data["name"],
        defaults={
            "address": restaurant_data.get("address", ""),
            "phone_number": restaurant_data.get("phone_number", ""),
            "email": restaurant_data.get("email", ""),
            "website": restaurant_data.get("website", ""),
        },
    )
    print("Restaurant created:", restaurant)

    # Determine the new version number
    latest_menu = (
        Menu.objects.filter(restaurant=restaurant).order_by("-version").first()
    )
    new_version_number = latest_menu.version + 1 if latest_menu else 1

    # Create the new menu
    menu = Menu.objects.create(
        restaurant=restaurant,
        name="Default Menu",  # Adjust as needed
        description="Generated menu",
        version=new_version_number,
        is_active=True,
    )
    print("Menu created:", menu)

    # Deactivate the previous active menu
    if latest_menu:
        latest_menu.is_active = False
        latest_menu.save()

    # Insert menu sections and items
    for section_data in menu_data["menus"]:
        section_name = section_data["section"]
        section_description = section_data.get("description", "")
        section_position = section_data.get("position", 0)

        menu_section = MenuSection.objects.create(
            menu=menu,
            name=section_name,
            description=section_description,
            position=section_position,
        )
        print("Menu section created:", menu_section)

        for item_data in section_data["items"]:
            food_item, created = FoodItem.objects.get_or_create(
                name=item_data["name"],
                defaults={
                    "description": item_data.get("description", ""),
                    "is_available": True,
                },
            )
            print("Food item created:", food_item)

            # Handle invalid price values
            try:
                price = Decimal(item_data.get("price", "0.00"))
            except (InvalidOperation, TypeError, ValueError) as e:
                print(f"Invalid price value: {item_data.get('price')}, error: {e}")
                price = Decimal("0.00")

            menu_item = MenuItem.objects.create(
                menu=menu,
                menu_section=menu_section,
                food_item=food_item,
                price=Decimal(price),
            )
            print("Menu item created:", menu_item)

            for restriction in item_data.get("dietary_restrictions", []):
                dietary_restriction, created = DietaryRestriction.objects.get_or_create(
                    name=restriction
                )
                FoodItemRestriction.objects.get_or_create(
                    food_item=food_item, dietary_restriction=dietary_restriction
                )
                print("Dietary restriction created or found:", dietary_restriction)

    # Log the processing action
    ProcessingLog.objects.create(
        menu=menu,
        action="Insert",
        description="Inserted menu data from JSON",
        performed_by="System",
    )
    print("Processing log created for menu:", menu)


def create_database_if_not_exists():
    try:
        connection = MySQLdb.connect(
            host=settings.DATABASES["default"]["HOST"],
            user=settings.DATABASES["default"]["USER"],
            passwd=settings.DATABASES["default"]["PASSWORD"],
            port=int(settings.DATABASES["default"]["PORT"]),
        )
        cursor = connection.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {settings.DATABASES['default']['NAME']}"
        )
        cursor.close()
        connection.close()
        print(
            f"Database {settings.DATABASES['default']['NAME']} created or already exists."
        )
    except MySQLdb.Error as e:
        print(f"Error creating database: {e}")


def check_mysql_connection():
    """
    Check if MySQL database connection is working.

    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        connection = MySQLdb.connect(
            host=settings.DATABASES["default"]["HOST"],
            user=settings.DATABASES["default"]["USER"],
            passwd=settings.DATABASES["default"]["PASSWORD"],
            db=settings.DATABASES["default"]["NAME"],
            port=int(settings.DATABASES["default"]["PORT"]),
        )
        connection.close()
        return True
    except MySQLdb.Error as e:
        print("Error connecting to MySQL:", e)
        return False
