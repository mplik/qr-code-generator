import qrcode
from PIL import Image

url = "https://mplik.eu"  # Wpisz tu swój adres

img = qrcode.make(url)
img.save("qr_code_mplik.png")
img.show()