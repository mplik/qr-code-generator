import qrcode
from PIL import Image

url = "https://github.com/mplik/domeny-web/raw/78cdb5e5220b65c2d41073aac366f228e49dcced/podfoldern/pdf/mplik_report_watermark_co2.pdf"  # Wpisz tu swój adres

img = qrcode.make(url)
img.save("qr_full_report.png")
img.show()

print("Plik został zapisany jako 'qr_full_report.png' w bieżącym katalogu")