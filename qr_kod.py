import qrcode
from PIL import Image
import os

url = "https://horizon.meta.com/profile/553955491139068/"  # Wpisz tu swój adres

# Upewnij się, że katalog istnieje
os.makedirs("docs/examples", exist_ok=True)

img = qrcode.make(url)
img.save("docs/examples/qr_meta_horizon.png")
img.show()

print("Plik został zapisany jako 'docs/examples/qr_meta_horizon.png'")