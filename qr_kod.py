import qrcode
from PIL import Image

url = "https://horizon.meta.com/profile/553955491139068/"  # Wpisz tu swój adres

img = qrcode.make(url)
img.save("qr_meta_horizon.png")
img.show()

print("Plik został zapisany jako 'qr_meta_horizon.png' w bieżącym katalogu")