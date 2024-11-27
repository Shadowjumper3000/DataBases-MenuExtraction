# menu/urls.py
from django.urls import path
from menu import views

urlpatterns = [
    path("", views.home, name="home"),  # Home page
    path("upload-pdf/", views.upload_pdf, name="upload_pdf"),  # PDF upload page
]
