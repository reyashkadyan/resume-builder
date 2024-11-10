from PyPDF2 import PdfReader

def extract_text_from_pdf_file(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""
    
def extract_text_from_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            return text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""