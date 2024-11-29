from django.urls import path
from .views import upload_pdf, process_text, home

urlpatterns = [
    path('upload-pdf/', upload_pdf, name='upload_pdf'),
    path('process-text/', process_text, name='process_text'),
    path('', home, name='home'),
]
