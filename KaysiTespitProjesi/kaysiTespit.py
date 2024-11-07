from ultralytics import YOLO
from roboflow import Roboflow


# YOLOv8 modelini başlat
model = YOLO('yolov8n.pt')

# Roboflow'dan API anahtarıyla veri indir
rf = Roboflow(api_key="HCwhuLCCr2K2GtY2YO37")
project = rf.workspace("malek-alkheder").project("kaysi_tespit")
version = project.version(1)
dataset = version.download("yolov8")

# İndirilen veri ile modeli eğit
if __name__ == "__main__" :
    model.train(data=f"{dataset.location}/data.yaml", epochs=1)