import cv2
import numpy as np
import matplotlib.pyplot as plt
import requests
from io import BytesIO

# URL'den resmi yüklemek için bir fonksiyon
def load_image_from_url(url):
    response = requests.get(url)
    image = np.asarray(bytearray(response.content), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image.astype(np.float32)

# Görselleri URL'lerden yükleme
square = load_image_from_url('https://image.winudf.com/v2/image/Y29tLkFsbWFrc29mdC5BQmx1ZUJveF9zY3JlZW5fMF9mNzg4cTJlMQ/screen-0.jpg?h=500&fakeurl=1&type=.jpg')
circle = load_image_from_url('https://norcalsps.com/cdn/shop/products/7531-fl-orange_1024x.jpg')

# Görselleri gri tonlamaya dönüştürme
square = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)
circle = cv2.cvtColor(circle, cv2.COLOR_BGR2GRAY)

# Yatay ve dikey filtrelerin ayarlanması
horizontal_kernel = np.array([[-1, 1]])
vertical_kernel = horizontal_kernel.T

# Yatay filtreyi uygulama
filter_horizontal_square = cv2.filter2D(square, -1, horizontal_kernel)
filter_horizontal_circle = cv2.filter2D(circle, -1, horizontal_kernel)

# Dikey filtreyi uygulama
filter_vertical_square = cv2.filter2D(square, -1, vertical_kernel)
filter_vertical_circle = cv2.filter2D(circle, -1, vertical_kernel)

# Kenar görüntüsü elde etmek için filtrelerin toplamını hesaplama
filter_square = np.sqrt(np.power(filter_horizontal_square, 2) + np.power(filter_vertical_square, 2))
filter_circle = np.sqrt(np.power(filter_horizontal_circle, 2) + np.power(filter_vertical_circle, 2))

# Sonuçları gösterme
plt.imshow(filter_square, cmap='gray')
plt.show()

plt.imshow(filter_circle, cmap='gray')
plt.show()
