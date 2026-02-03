import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

url = "https://mplik.eu"   # Wpisz tu swój adres
opis = "giełda domen"      # Podpis pod kodem QR
filename = "outputs/qr_mplik_podpis.png"  # Nazwa pliku do zapisu

# Upewnij się, że katalog istnieje
os.makedirs("outputs", exist_ok=True)

# Generowanie kodu QR
img = qrcode.make(url).convert('RGB')

# Ustalanie rozmiarów
szerokosc, wysokosc = img.size
wysokosc_podpisu = 40

# Tworzenie nowego obrazka z miejscem na podpis
img_podpis = Image.new('RGB', (szerokosc, wysokosc + wysokosc_podpisu), 'white')
img_podpis.paste(img, (0, 0))

# Dodawanie tekstu
draw = ImageDraw.Draw(img_podpis)
try:
    font = ImageFont.truetype("segoeui.ttf", 28)
except:
    font = ImageFont.load_default()

# Obliczanie pozycji tekstu (textbbox zamiast przestarzałego textsize)
bbox = draw.textbbox((0, 0), opis, font=font)
szer_napisu = bbox[2] - bbox[0]
wys_napisu = bbox[3] - bbox[1]
x = (szerokosc - szer_napisu) // 2
y = wysokosc + (wysokosc_podpisu - wys_napisu) // 2
draw.text((x, y), opis, font=font, fill='black')

img_podpis.save(filename)
img_podpis.show()

print(f"Plik został zapisany jako '{filename}'")
