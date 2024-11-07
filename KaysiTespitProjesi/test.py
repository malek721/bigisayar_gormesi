import os
import requests
from ultralytics import YOLO

# YOLO modelini yükle
model = YOLO(r'C:\Users\admin\PycharmProjects\KaysiTespitProjesi\runs\detect\train\weights/best.pt')

# Görsel URL'si
source_url = "https://littlerock.com.mt/wp-content/uploads/2015/03/apricots.jpg"

# URL'den görseli indir ve geçici bir dosyaya kaydet
image_path = "temp_image.jpg"
response = requests.get(source_url)
with open(image_path, "wb") as file:
    file.write(response.content)

# Sonuçların kaydedileceği klasörü oluştur
results_folder = "results"
os.makedirs(results_folder, exist_ok=True)

# Model ile tahmin yap ve sonucu kaydet
results = model.predict(source=image_path, conf=0.45, iou=0.45)

# Tahmin edilen görseli 'results' klasörüne kaydet
results[0].save(os.path.join(results_folder, "prediction_from_url.jpg"))
print("Görsel işlendi - Sonuçlar 'results' klasöründe 'prediction_from_url.jpg' olarak kaydedildi")

# Geçici görsel dosyasını sil
os.remove(image_path)
