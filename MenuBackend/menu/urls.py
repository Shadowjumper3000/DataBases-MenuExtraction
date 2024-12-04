from django.urls import path
from . import views

urlpatterns = [
    path("process-text/", views.process_text, name="process_text"),  # Process text
    path("", views.home, name="home"),  # Home page
    path("upload-pdf/", views.upload_pdf, name="upload_pdf"),  # PDF upload page
    path("upload-json/", views.upload_json, name="upload_json"),  # JSON upload page
    path("restaurants/", views.restaurant_list, name="restaurant_list"),  # Restaurant list page
    path("restaurants/<int:restaurant_id>/", views.restaurant_detail, name="restaurant_detail"),  # Restaurant detail page
    path("filter-menu/", views.filter_menu_items, name="filter_menu_items"),  # Filter menu items
    path("reports/", views.reports_home, name="reports_home"),  # Reports home page
    path("reports/menus/", views.menu_report, name="menu_report"),  # Menu report
    path("reports/menu-items/", views.menu_item_report, name="menu_item_report"),  # Menu item report
    path("reports/food-item-restrictions/", views.food_item_restriction_report, name="food_item_restriction_report"),  # Food item restriction report
    path("reports/processing-logs/", views.processing_log_report, name="processing_log_report"),  # Processing log report
    path("reports/active-menus/", views.active_menu_report, name="active_menu_report"),  # Active menu report
]
