import fitz
from langchain_core.documents import Document
import re
import pytesseract
from PIL import Image
import io



# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def clean_text(text:str):
        text=re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'[|•▪\t]', ' ', text)
        return text.strip()


def extract_text_from_pdf(pdf_path,file_name):
    document = fitz.open(pdf_path)
    extracted_text = []
    for page_num,page in enumerate(document):
        text = page.get_text().strip()
        if text:
            extracted_text.append(Document(page_content=clean_text(text), metadata={"file_name":file_name, "page_number": page_num, "source":"text"}))
        else :
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            ocr_text = pytesseract.image_to_string(img)
            if ocr_text.strip():
                extracted_text.append(Document(page_content=clean_text(ocr_text), metadata={"file_name":file_name, "page_number": page_num, "source":"ocr"}))
            else:
                extracted_text.append(Document(page_content="", metadata={"file_name":file_name, "page_number": page_num, "source":"empty"}))
    document.close()
    return extracted_text




