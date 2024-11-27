from django.shortcuts import render, redirect
from .forms import PDFUploadForm
from .models import PDFUpload
from .utils import extract_text_from_pdf
from database_handler.utils import insert_menu_data
from django.conf import settings

import MySQLdb
import requests
