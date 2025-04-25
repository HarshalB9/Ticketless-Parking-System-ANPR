import cv2
import easyocr

reader = easyocr.Reader(['en'])

def get_plate_number(image_path):
    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = reader.readtext(rgb)

    texts = [text for (_bbox, text, conf) in results]
    if not texts:
        raise ValueError("No text detected.")
    
    return "".join(texts).replace(" ", "").upper()
