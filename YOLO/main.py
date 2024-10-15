import numpy as np
from ultralytics import YOLO
import cv2

model = YOLO('yolov8l.pt')
image = cv2.imread(r"C:\Users\admin\Desktop\galery\car.jpeg")
results = model(image, conf=0.4)

if isinstance(results, list):
    results = results[0]

if hasattr(results, 'show'):
    results.show()

results.save('results/')
boxes = results.boxes
df = []

for box in boxes:
    x1, y1, x2, y2 = box.xyxy[0].tolist()
    confidence = box.conf.tolist()[0]
    class_id = box.cls.tolist()[0]
    df.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'confidence': confidence, 'class_id': class_id})

for detection in df:
    print(detection)

