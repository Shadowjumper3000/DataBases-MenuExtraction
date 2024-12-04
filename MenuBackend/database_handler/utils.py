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

def insert_menu_data(menu_data):
    print("Inserting menu data:", menu_data)

    # Insert restaurant data
    restaurant_data = menu_data["restaurant"]
    restaurant, created = Restaurant.objects.get_or_create(
        name=restaurant_data["name"],
        defaults={
            "address": restaurant_data["address"],
            "phone_number": restaurant_data["phone_number"],
            "email": restaurant_data["email"],
            "website": restaurant_data["website"],
        },
    )
    print("Restaurant created:", restaurant)

    # Determine the new version number
    latest_menu = Menu.objects.filter(restaurant=restaurant).order_by('-version').first()
    new_version_number = latest_menu.version + 1 if latest_menu else 1

    # Serialize the latest menu data to compare with the new menu data
    def serialize_menu(menu):
        menu_sections = MenuSection.objects.filter(menu=menu)
        sections_data = []
        for section in menu_sections:
            items = MenuItem.objects.filter(menu_section=section)
            items_data = [
                {
                    "name": item.food_item.name,
                    "description": item.food_item.description,
                    "price": float(item.price),
                    "dietary_restrictions": [
                        restriction.dietary_restriction.name
                        for restriction in item.food_item.fooditemrestriction_set.all()
                    ],
                }
                for item in items
            ]
            sections_data.append({
                "section": section.name,
                "description": section.description,
                "position": section.position,
                "items": items_data,
            })
        return {
            "restaurant": {
                "name": menu.restaurant.name,
                "address": menu.restaurant.address,
                "phone_number": menu.restaurant.phone_number,
                "email": menu.restaurant.email,
                "website": menu.restaurant.website,
            },
            "menus": sections_data,
        }

    # Check if the new menu data is the same as the latest menu data
    if latest_menu:
        latest_menu_data = serialize_menu(latest_menu)
        if json.dumps(latest_menu_data, sort_keys=True) == json.dumps(menu_data, sort_keys=True):
            # Log the new version without creating duplicates
            ProcessingLog.objects.create(
                menu=latest_menu,
                action="Version",
                description=f"Version {new_version_number} logged without changes",
                performed_by="System",
            )
            print(f"Version {new_version_number} logged without changes for menu:", latest_menu)
            return

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
                defaults={"description": item_data.get("description", ""), "is_available": True},
            )
            print("Food item created:", food_item)

            MenuItem.objects.create(
                menu=menu,
                menu_section=menu_section,
                food_item=food_item,
                price=item_data.get("price", 0.00),
            )
            print("Menu item created:", MenuItem)

            for restriction in item_data.get("dietary_restrictions", []):
                dietary_restriction, created = DietaryRestriction.objects.get_or_create(name=restriction)
                FoodItemRestriction.objects.get_or_create(food_item=food_item, dietary_restriction=dietary_restriction)
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