import qrcode
from PIL import Image

url = "https://github.com/mplik/domeny-web/raw/79a7c3a55d9464a4ef671306edb52e07f331d73a/podfoldern/pdf/wykres_kolowy_z_opisem.pdf"  # Wpisz tu swój adres

img = qrcode.make(url)
img.save("qr_wykres.png")
img.show()

print("Plik został zapisany jako 'qr_wykres_kolowy.png' w bieżącym katalogu")