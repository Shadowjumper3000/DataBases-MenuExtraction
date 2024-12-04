from django import forms


class PDFUploadForm(forms.Form):
    """
    A form for uploading PDF files.

    Attributes:
        file (FileField): A file field for selecting the PDF file to upload.
    """

    file = forms.FileField()
