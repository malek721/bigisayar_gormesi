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

# إعداد السائق لمتصفح Microsoft Edge
driver = webdriver.Edge()

# تسجيل الدخول إلى فيسبوك
driver.get("https://www.facebook.com/")
time.sleep(2)  # انتظر تحميل الصفحة

# إدخال بيانات تسجيل الدخول
email_input = driver.find_element(By.ID, "email")
email_input.send_keys("malekco721@gmail.com")

password_input = driver.find_element(By.ID, "pass")
password_input.send_keys("malek2002kh")
password_input.send_keys(Keys.RETURN)

# الانتظار حتى تحميل الصفحة الرئيسية
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='navigation']"))
    )
    print("تم تحميل الصفحة الرئيسية بنجاح.")
except Exception as e:
    print("فشل في تحميل الصفحة الرئيسية:", e)

# قراءة روابط الحسابات من ملف إكسل
excel_file = r'C:\Users\admin\Desktop\bilgisayar gormesi\facebook_acounts.xlsx'  # قم بتعديل اسم الملف حسب الحاجة
df = pd.read_excel(excel_file)

# إنشاء مجلد لحفظ الصور إذا لم يكن موجودًا
output_folder = "profile_pictures"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# معالجة كل رابط في ملف الإكسل
for index, row in df.iterrows():
    profile_url = row['Profile URL']  # تأكد من أن هذا هو اسم العمود الصحيح
    driver.get(profile_url)

    # الانتظار لتأكيد تحميل الصفحة
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h1"))
        )
        print(f"تم تحميل صفحة المستخدم {profile_url} بنجاح.")
    except Exception as e:
        print(f"فشل في تحميل صفحة المستخدم {profile_url}:", e)
        continue

    # الانتظار لمدة 5 ثوانٍ قبل تنفيذ JavaScript
    time.sleep(5)

    # محاولة استخدام JavaScript لاستخراج رابط الصورة من داخل SVG
    try:
        profile_image_url = driver.execute_script("""
        // اختيار جميع عناصر SVG التي تحتوي على الصور
        let svgElements = document.querySelectorAll('svg[role="img"] image');
        if (svgElements.length > 1) { // التأكد من وجود أكثر من صورة
            return svgElements[1].getAttribute('xlink:href'); // إرجاع رابط الصورة الثانية
        }
        return null; // إرجاع null إذا لم يتم العثور على صورة ثانية
        """)

        # التحقق من القيمة المستخرجة
        if profile_image_url:
            print("رابط صورة البروفايل:", profile_image_url)

            # تنزيل الصورة إذا تم العثور على الرابط
            img_response = requests.get(profile_image_url)
            if img_response.status_code == 200:
                # حفظ الصورة في المجلد المحدد
                image_filename = os.path.join(output_folder, f"profile_picture_{index + 1}.jpg")
                with open(image_filename, "wb") as f:
                    f.write(img_response.content)
                print(f"تم تنزيل صورة البروفايل بنجاح وحفظها كـ {image_filename}.")
            else:
                print(f"فشل في تنزيل صورة البروفايل. حالة الاستجابة:", img_response.status_code)
        else:
            print("لم يتم العثور على صورة البروفايل.")

    except Exception as e:
        print("فشل في تحميل صورة البروفايل:", e)

# إغلاق المتصفح
driver.quit()

from ultralytics import YOLO
import cv2
import os

# تحميل نموذج YOLO
model = YOLO('yolov8l.pt')

# تحديد المجلد الذي يحتوي على صور البروفايل
folder_path = r"C:\Users\admin\PycharmProjects\Facebook Profil Resmi Analizi\profile_pictures"  # تأكد من وضع المسار الصحيح للمجلد

# استعراض جميع الملفات في المجلد
for filename in os.listdir(folder_path):
    # التأكد من أن الملف هو صورة
    if filename.endswith(('.png', '.jpg', '.jpeg')):  # يمكنك إضافة المزيد من أنواع الملفات إذا لزم الأمر
        # قراءة الصورة
        image_path = os.path.join(folder_path, filename)
        image = cv2.imread(image_path)

        # استخدام نموذج YOLO لفحص الصورة
        results = model(image, conf=0.4)

        if isinstance(results, list):
            results = results[0]

        # عرض النتائج
        if hasattr(results, 'show'):
            print(f"فحص الصورة: {filename}")
            results.show()

