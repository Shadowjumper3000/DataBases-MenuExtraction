from django.db import models

class PDFUpload(models.Model):
    """
    Model to store PDF file uploads and associated metadata.
    
    Fields:
    - file: The uploaded PDF file.
    - uploaded_at: Timestamp for when the file was uploaded.
    """
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the PDFUpload model.
        Returns the name of the uploaded file.
        """
        return self.file.name
