from PIL import Image
from pytesseract import pytesseract


def image_to_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text
