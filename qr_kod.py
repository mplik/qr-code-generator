import qrcode
from PIL import Image
import os

url = "https://horizon.meta.com/profile/553955491139068/"  # Wpisz tu swój adres
filename = "docs/examples/qr_meta_horizon.png"  # Nazwa pliku do zapisu

# Upewnij się, że katalog istnieje
os.makedirs("docs/examples", exist_ok=True)

img = qrcode.make(url)
img.save(filename)
img.show()

print(f"Plik został zapisany jako '{filename}'")