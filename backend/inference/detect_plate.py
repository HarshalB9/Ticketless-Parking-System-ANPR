from ultralytics import YOLO
import cv2

model = YOLO("best.pt")

def detect_plate(image_path):
    image = cv2.imread(image_path)
    results = model(image)
    
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            plate = image[y1:y2, x1:x2]
            cv2.imwrite("plate.jpg", plate)
