import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

url = "https://rabinem6.fakturownia.pl/u/partner"   # Wpisz tu swój adres
opis = "Faktury QR"      # Podpis pod kodem QR
filename = "outputs/faktury_qr.png"  # Nazwa pliku do zapisu
filename_onedrive = r"C:\Users\Dell\OneDrive\kod qr\mplik_kody_qr_github\faktury_qr.png"  # Kopia na OneDrive

# Upewnij się, że katalogi istnieją
os.makedirs("outputs", exist_ok=True)
os.makedirs(r"C:\Users\Dell\OneDrive\kod qr\mplik_kody_qr_github", exist_ok=True)

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
img_podpis.save(filename_onedrive)  # Zapisz też na OneDrive
img_podpis.show()

print(f"Plik został zapisany jako '{filename}'")
print(f"Kopia zapisana w: '{filename_onedrive}'")
