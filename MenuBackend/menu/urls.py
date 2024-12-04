from django.urls import path
from . import views

urlpatterns = [
    path("process-text/", views.process_text, name="process_text"),
    path("", views.home, name="home"),
    path("upload-pdf/", views.upload_pdf, name="upload_pdf"),
    path("upload-json/", views.upload_json, name="upload_json"),
    path("restaurants/", views.restaurant_list, name="restaurant_list"),
    path("restaurants/<int:restaurant_id>/", views.restaurant_detail, name="restaurant_detail"),
    path("filter-menu/", views.filter_menu_items, name="filter_menu_items"),
    path("filter-foods/", views.filter_foods_by_restrictions, name="filter_foods_by_restrictions"),
    path("filter-restrictions/", views.filter_restrictions_by_food, name="filter_restrictions_by_food"),
    path("reports/", views.reports_home, name="reports_home"),

]
