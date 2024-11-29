from django.test import TestCase
from decimal import Decimal
from .models import (
    Restaurant,
    Menu,
    MenuSection,
    MenuItem,
    DietaryRestriction,
    ItemRestriction,
)
from .utils import insert_menu_data


class MenuDataInsertionTest(TestCase):
    def setUp(self):
        self.menu_data = {
            "restaurant": {
                "name": "Test Restaurant",
                "address": "123 Test St",
                "phone_number": "123-456-7890",
                "email": "test@example.com",
                "website": "http://www.testrestaurant.com",
            },
            "menus": [
                {
                    "section": "Appetizers",
                    "items": [
                        {
                            "name": "Spring Rolls",
                            "description": "Crispy rolls with vegetables",
                            "price": 5.99,
                            "dietary_restrictions": ["Vegetarian"],
                        }
                    ],
                }
            ],
        }

    def test_insert_menu_data(self):
        # Insert the menu data
        insert_menu_data(self.menu_data)

        # Verify the restaurant was created
        restaurant = Restaurant.objects.get(name="Test Restaurant")
        self.assertIsNotNone(restaurant)
        self.assertEqual(restaurant.address, "123 Test St")
        self.assertEqual(restaurant.phone_number, "123-456-7890")
        self.assertEqual(restaurant.email, "test@example.com")
        self.assertEqual(restaurant.website, "http://www.testrestaurant.com")

        # Verify the menu was created
        menu = Menu.objects.get(restaurant=restaurant)
        self.assertIsNotNone(menu)
        self.assertEqual(menu.name, "Default Menu")
        self.assertEqual(menu.description, "Generated menu")

        # Verify the menu section was created
        section = MenuSection.objects.get(menu=menu, name="Appetizers")
        self.assertIsNotNone(section)
        self.assertEqual(section.name, "Appetizers")

        # Verify the menu item was created
        menu_item = MenuItem.objects.get(menu_section=section, name="Spring Rolls")
        self.assertIsNotNone(menu_item)
        self.assertEqual(menu_item.description, "Crispy rolls with vegetables")
        self.assertEqual(menu_item.price, Decimal("5.99"))

        # Verify the dietary restriction was created
        dietary_restriction = DietaryRestriction.objects.get(name="Vegetarian")
        self.assertIsNotNone(dietary_restriction)

        # Verify the item restriction was created
        item_restriction = ItemRestriction.objects.get(
            menu_item=menu_item, dietary_restriction=dietary_restriction
        )
        self.assertIsNotNone(item_restriction)

        # Print the data to inspect it
        print("Restaurant:", Restaurant.objects.all())
        print("Menu:", Menu.objects.all())
        print("MenuSection:", MenuSection.objects.all())
        print("MenuItem:", MenuItem.objects.all())
        print("DietaryRestriction:", DietaryRestriction.objects.all())
        print("ItemRestriction:", ItemRestriction.objects.all())

        # Pause to inspect the database
        input("Press Enter to continue...")
