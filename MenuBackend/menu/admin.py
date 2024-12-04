from django.contrib import admin
from database_handler.models import (
    Restaurant,
    Menu,
    MenuSection,
    MenuItem,
    FoodItem,
    DietaryRestriction,
    FoodItemRestriction,
    ProcessingLog,
)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'email', 'website', 'created_at', 'updated_at')
    search_fields = ('name', 'address', 'phone_number', 'email', 'website')

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'name', 'description', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'restaurant')

@admin.register(MenuSection)
class MenuSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'position', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('position',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('menu', 'menu_section', 'food_item', 'price')
    search_fields = ('food_item__name', 'menu__name', 'menu_section__name')
    list_filter = ('menu', 'menu_section')

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_available')
    search_fields = ('name', 'description')
    list_filter = ('is_available',)

@admin.register(DietaryRestriction)
class DietaryRestrictionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(FoodItemRestriction)
class FoodItemRestrictionAdmin(admin.ModelAdmin):
    list_display = ('food_item', 'dietary_restriction')
    search_fields = ('food_item__name', 'dietary_restriction__name')
    list_filter = ('dietary_restriction',)

@admin.register(ProcessingLog)
class ProcessingLogAdmin(admin.ModelAdmin):
    list_display = ('menu', 'action', 'description', 'performed_by', 'action_time')
    search_fields = ('menu__name', 'action', 'description', 'performed_by')
    list_filter = ('action', 'performed_by')