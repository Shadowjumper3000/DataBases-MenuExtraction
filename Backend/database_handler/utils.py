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

    # Create a menu for the restaurant
    menu = Menu.objects.create(
        restaurant=restaurant,
        name="Default Menu",  # Adjust as needed
        description="Generated menu",
    )
    print("Menu created:", menu)

    # Insert menu sections and items
    for section_data in menu_data["menus"]:
        section, created = MenuSection.objects.get_or_create(
            name=section_data["section"],
            defaults={
                "description": "",
                "position": 0,  # Adjust as needed
            },
        )
        print("Menu section created:", section)

        for item_data in section_data["items"]:
            # Create or get the food item
            food_item, created = FoodItem.objects.get_or_create(
                name=item_data["name"],
                defaults={
                    "description": item_data.get("description", ""),
                    "is_available": True,  # Adjust as needed
                },
            )
            print("Food item created:", food_item)

            # Create the menu item linking the food item, menu, menu section, and price
            menu_item = MenuItem.objects.create(
                menu=menu,
                menu_section=section,
                food_item=food_item,
                price=item_data.get("price", 0.00),  # Set price here
            )
            print("Menu item created:", menu_item)

            # Insert dietary restrictions
            for restriction in item_data.get("dietary_restrictions", []):
                dietary_restriction, created = DietaryRestriction.objects.get_or_create(
                    name=restriction
                )
                FoodItemRestriction.objects.create(
                    food_item=food_item, dietary_restriction=dietary_restriction
                )
                print("Dietary restriction created:", dietary_restriction)

    # Log the processing action
    ProcessingLog.objects.create(
        menu=menu,
        action="Insert",
        description="Inserted menu data from JSON",
        performed_by="System",  # Adjust as needed
    )
    print("Processing log created for menu:", menu)


def create_database_if_not_exists():
    db_settings = settings.DATABASES["default"]
    db_name = db_settings["NAME"]
    connection = MySQLdb.connect(
        host=db_settings["HOST"],
        user=db_settings["USER"],
        passwd=db_settings["PASSWORD"],
        port=int(db_settings["PORT"]),
    )
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.close()
    connection.close()


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
