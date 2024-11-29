from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import PDFUpload
from database_handler.models import Restaurant, Menu, MenuSection, MenuItem


class PDFUploadTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload_url = reverse("upload_pdf")

    def test_pdf_upload(self):
        # Create a sample PDF file
        pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT /F1 24 Tf 100 700 Td (Hello, World!) Tj ET\nendstream\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
        pdf_file = SimpleUploadedFile(
            "test.pdf", pdf_content, content_type="application/pdf"
        )

        # Upload the PDF file
        response = self.client.post(self.upload_url, {"file": pdf_file})

        # Check that the upload was successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "menu/pdf_upload_success.html")

        # Check that the PDF file was saved in the database
        self.assertEqual(PDFUpload.objects.count(), 1)
        pdf_upload = PDFUpload.objects.first()
        self.assertEqual(pdf_upload.file.name, "pdfs/test.pdf")

        # Check that the extracted text is correct
        self.assertIn("Hello, World!", response.context["extracted_text"])

        # Check that the menu data was inserted into the database
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Menu.objects.count(), 1)
        self.assertEqual(MenuSection.objects.count(), 1)
        self.assertEqual(MenuItem.objects.count(), 1)
