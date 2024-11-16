import tkinter as tk
from tkinter import filedialog, messagebox
import segno
from PIL import Image, ImageTk

def generate_and_display_qr():
    # Kullanıcıdan alınan bağlantıyı al ve boşlukları temizle
    link = entry.get().strip()
    if not link:
        messagebox.showerror("Hata", "Lütfen bir bağlantı girin.")
        return

    # Bağlantının başında "http://" veya "https://" yoksa, otomatik olarak ekle
    if not link.startswith(("http://", "https://")):
        link = "https://" + link

    try:
        # Yüksek hata düzeltmeli QR Code oluşturma
        qr = segno.make(link, error='H')  # Hata düzeltme eklendi
        qr.save("qrcode_temp.png", scale=10)
        img = ImageTk.PhotoImage(Image.open("qrcode_temp.png"))
        qr_label.config(image=img)
        qr_label.image = img
    except Exception as e:
        # Hata durumunda kullanıcıya mesaj gösterme
        messagebox.showerror("Hata", f"QR Code oluşturulurken bir hata oluştu: {e}")

def save_qr():
    # Kullanıcıdan alınan bağlantıyı al ve boşlukları temizle
    link = entry.get().strip()
    if not link:
        messagebox.showerror("Hata", "Önce QR Code oluşturmanız gerekiyor.")
        return

    # Bağlantının başında "http://" veya "https://" yoksa, otomatik olarak ekle
    if not link.startswith(("http://", "https://")):
        link = "https://" + link

    # Dosya kaydetme konumunu kullanıcıya sor
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG dosyaları", "*.png")])
    if file_path:
        # Yüksek hata düzeltmeli QR Code'u kaydetme
        segno.make(link, error='H').save(file_path, scale=10)  # Hata düzeltme eklendi
        messagebox.showinfo("Kaydedildi", f"QR Code kaydedildi: {file_path}")

# Ana arayüz penceresi oluşturma
root = tk.Tk()
root.title("QR Code Oluşturucu")

# Bağlantı giriş alanı
tk.Label(root, text="Bağlantıyı girin:").pack(pady=5)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

# QR Code oluşturma butonu
tk.Button(root, text="QR Code Oluştur", command=generate_and_display_qr).pack(pady=5)

# QR Code kaydetme butonu
tk.Button(root, text="QR Code'u Kaydet", command=save_qr).pack(pady=5)

# QR Code görüntüsü için alan
qr_label = tk.Label(root)
qr_label.pack(pady=10)

# Uygulamayı çalıştırma
root.mainloop()
