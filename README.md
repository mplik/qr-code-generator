# QR Code Generator

Prosty generator kodów QR w języku Python, który tworzy kod QR z podanego adresu URL.

## Opis

Skrypt generuje kod QR na podstawie wprowadzonego adresu URL i zapisuje go jako plik PNG. Kod QR można następnie zeskanować telefonem, aby szybko przejść do zapisanego adresu.

## Wymagania

- Python 3.x
- Biblioteka `qrcode`
- Biblioteka `Pillow` (PIL)

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone https://github.com/mplik/qr-code-generator.git
cd qr-code-generator
```

2. Zainstaluj wymagane biblioteki:
```bash
pip install qrcode[pil]
```

lub w środowisku wirtualnym:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac
pip install qrcode[pil]
```

## Użycie

1. Edytuj plik `qr_kod.py` i wpisz swój adres URL w zmiennej `url`:
```python
url = "https://twoj-adres.com"
```

2. Uruchom skrypt:
```bash
python qr_kod.py
```

3. Kod QR zostanie zapisany w katalogu `docs/examples/qr_meta_horizon.png` i automatycznie otworzy się w domyślnej przeglądarce obrazów.

## Przykład

![Przykładowy kod QR dla EL-QR Studio](static/examples/el_qr_studio.png)

*Przykładowy kod QR wygenerowany dla "EL-QR Studio"*

```python
import qrcode
from PIL import Image
import os

url = "https://horizon.meta.com/profile/553955491139068/"

# Upewnij się, że katalog istnieje
os.makedirs("docs/examples", exist_ok=True)

img = qrcode.make(url)
img.save("docs/examples/qr_meta_horizon.png")
img.show()

print("Plik został zapisany jako 'docs/examples/qr_meta_horizon.png'")
```

## Funkcje

### Podstawowa wersja (qr_kod.py)
- ✅ Generowanie kodu QR z dowolnego adresu URL
- ✅ Automatyczne zapisywanie jako plik PNG
- ✅ Wyświetlanie wygenerowanego kodu QR
- ✅ Prosty i szybki w użyciu

### Zaawansowana wersja (qr_generator_v2.py)
- ✅ Wszystkie funkcje podstawowej wersji
- ✅ Dodawanie niestandardowego podpisu pod kodem QR
- ✅ Automatyczna konfiguracja katalogu wyjściowego (outputs/)
- ✅ Opcjonalne zapisywanie kopii na OneDrive
- ✅ Profesjonalna czcionka Segoe UI dla tekstu
- ✅ Nowoczesne API PIL (textbbox)

## Użycie wersji v2

### Szybki start

1. Edytuj plik `qr_generator_v2.py` i ustaw parametry:
```python
url = "https://twoj-adres.com"      # Twój adres URL
opis = "Nazwa QR"                    # Podpis pod kodem QR
filename = "outputs/twoj_qr.png"    # Ścieżka zapisu
```

2. Uruchom skrypt:
```bash
python qr_generator_v2.py
```

3. Kod QR z podpisem zostanie zapisany w katalogu `outputs/` i automatycznie się otworzy.

### Pełny przykład

```python
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

url = "https://rabinem6.fakturownia.pl/u/partner"
opis = "Faktury QR"
filename = "outputs/faktury_qr.png"

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

# Obliczanie pozycji tekstu (wyśrodkowanie)
bbox = draw.textbbox((0, 0), opis, font=font)
szer_napisu = bbox[2] - bbox[0]
wys_napisu = bbox[3] - bbox[1]
x = (szerokosc - szer_napisu) // 2
y = wysokosc + (wysokosc_podpisu - wys_napisu) // 2
draw.text((x, y), opis, font=font, fill='black')

img_podpis.save(filename)
img_podpis.show()

print(f"Plik został zapisany jako '{filename}'")
```

## Autor

[mplik](https://github.com/mplik)

## Licencja

MIT License
