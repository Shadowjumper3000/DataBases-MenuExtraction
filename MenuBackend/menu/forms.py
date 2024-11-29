from django import forms
from .models import PDFUpload


class PDFUploadForm(forms.ModelForm):
    """
    Form to handle file uploads for PDFs.

    The form uses the `PDFUpload` model to allow users to upload PDF files.
    """

    class Meta:
        model = PDFUpload
        fields = ["file"]

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and add custom attributes to the fields.

        Args:
        - *args: Variable length argument list.
        - **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.fields["file"].widget.attrs.update({"class": "form-control"})
