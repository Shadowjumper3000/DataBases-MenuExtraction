import pdfplumber


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using pdfplumber.

    Args:
    - pdf_path: Path to the PDF file on the server.

    Returns:
    - A string containing the extracted text from the PDF file.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text
