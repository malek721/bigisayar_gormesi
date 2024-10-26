from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import pandas as pd
import openpyxl
import os
from ultralytics import YOLO
import cv2

# Microsoft Edge tarayıcısını başlatma
driver = webdriver.Edge()

# Facebook’a giriş yapma
driver.get("https://www.facebook.com/")
time.sleep(2)  # Sayfanın yüklenmesini bekle

# Giriş bilgilerini girme
email_input = driver.find_element(By.ID, "email")
email_input.send_keys("")                                   #<----- mail adres yada kullanci ismi

password_input = driver.find_element(By.ID, "pass")
password_input.send_keys("")                                #<----- sifre
password_input.send_keys(Keys.RETURN)

# Ana sayfanın yüklenmesini bekleme
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='navigation']"))
    )
    print("Ana sayfa başarıyla yüklendi.")
except Exception as e:
    print("Ana sayfa yüklenemedi:", e)

# Hesap linklerini Excel dosyasından okuma
excel_file = r'facebook_acounts.xlsx'
df = pd.read_excel(excel_file)

# Resimleri kaydetmek için bir klasör oluşturma
output_folder = "profile_pictures"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Excel dosyasındaki her bağlantıyı işleme
for index, row in df.iterrows():
    profile_url = row['Profile URL']  # Bu sütunun adının doğru olduğundan emin olun
    driver.get(profile_url)

    # Sayfanın yüklendiğini doğrulamak için bekleme
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h1"))
        )
        print(f"Kullanıcı sayfası {profile_url} başarıyla yüklendi.")
    except Exception as e:
        print(f"Kullanıcı sayfası {profile_url} yüklenemedi:", e)
        continue

    # JavaScript'i çalıştırmadan önce 5 saniye bekle
    time.sleep(5)

    # SVG içinden profil resmi bağlantısını almak için JavaScript kullanma
    try:
        profile_image_url = driver.execute_script("""
        // Resimleri içeren tüm SVG öğelerini seç
        let svgElements = document.querySelectorAll('svg[role="img"] image');
        if (svgElements.length > 1) { // Birden fazla resim olduğundan emin ol
            return svgElements[1].getAttribute('xlink:href'); // İkinci resmin bağlantısını döndür
        }
        return null; // İkinci resim bulunmazsa null döndür
        """)

        # Çıkarılan değeri kontrol etme
        if profile_image_url:
            print("Profil resim bağlantısı:", profile_image_url)

            # Bağlantı bulunursa resmi indirme
            img_response = requests.get(profile_image_url)
            if img_response.status_code == 200:
                # Resmi belirtilen klasöre kaydet
                image_filename = os.path.join(output_folder, f"profile_picture_{index + 1}.jpg")
                with open(image_filename, "wb") as f:
                    f.write(img_response.content)
                print(f"Profil resmi başarıyla indirildi ve {image_filename} olarak kaydedildi.")
            else:
                print(f"Profil resmi indirilemedi. Yanıt durumu:", img_response.status_code)
        else:
            print("Profil resmi bulunamadı.")

    except Exception as e:
        print("Profil resmi yüklenemedi:", e)

# Tarayıcıyı kapatma
driver.quit()

# YOLO modelini yükleme
model = YOLO('yolov8l.pt')

# Profil resimlerinin bulunduğu klasörü belirtme
folder_path = 'profile_pictures/'

# Klasördeki tüm dosyaları listeleme
for filename in os.listdir(folder_path):
    # Dosyanın bir resim olduğundan emin ol
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        # Resmi okuma
        image_path = os.path.join(folder_path, filename)
        image = cv2.imread(image_path)

        # Resmi YOLO modeli ile tarama
        results = model(image, conf=0.4)

        if isinstance(results, list):
            results = results[0]

        # Sonuçları gösterme
        if hasattr(results, 'show'):
            print(f"Resim tarandı: {filename}")
            results.show()
