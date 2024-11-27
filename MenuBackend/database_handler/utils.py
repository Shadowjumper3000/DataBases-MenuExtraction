from .models import Restaurant, Menu, MenuSection, MenuItem
from django.conf import settings
import MySQLdb


def insert_menu_data(menu_data):
    restaurant, created = Restaurant.objects.get_or_create(
        name="Default Restaurant",  # Adjust as needed
        defaults={"address": "Default Address"},
    )

    menu = Menu.objects.create(
        restaurant=restaurant,
        name="Default Menu",  # Adjust as needed
        description="Generated menu",
    )

    for section_data in menu_data["menus"]:
        section = MenuSection.objects.create(
            menu=menu, name=section_data["section"], position=0  # Adjust as needed
        )

        for item_data in section_data["items"]:
            MenuItem.objects.create(
                menu_section=section,
                name=item_data,
                description="",
                price=0.00,  # Adjust as needed
            )


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
        print(f"Error connecting to MySQL: {e}")
        return False
