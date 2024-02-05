from PIL import Image
import pytesseract
import requests
from io import BytesIO
def image_to_text(ImageURL):
    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        }
    response = requests.get(ImageURL, stream = True, headers=header)
    #add path to tesseract
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if response.status_code != 200:
        return None
    img = Image.open(BytesIO(response.content))
    pytesseract.pytesseract.tesseract_cmd = path_to_tesseract
    text = pytesseract.image_to_string(img)
    return text
# print((image_to_text("http://www.teamjimmyjoe.com/wp-content/uploads/2014/09/Classic-Best-Funny-Text-Messages-earthquake-titties.jpg")))