from django.urls import path
from menu import views

urlpatterns = [
    path("", views.home, name="home"),  # Home page
    path("upload-pdf/", views.upload_pdf, name="upload_pdf"),  # PDF upload page
    path("upload-json/", views.upload_json, name="upload_json"),  # JSON upload page
    path(
        "restaurants/", views.restaurant_list, name="restaurant_list"
    ),  # Restaurant list page
    path(
        "restaurants/<int:restaurant_id>/",
        views.restaurant_detail,
        name="restaurant_detail",
    ),  # Restaurant detail page
]
