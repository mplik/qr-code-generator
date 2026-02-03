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

3. Kod QR zostanie zapisany w katalogu `docs/exampels/qr_meta_horizon.png` i automatycznie otworzy się w domyślnej przeglądarce obrazów.

## Przykład

```python
import qrcode
from PIL import Image
import os

url = "https://horizon.meta.com/profile/553955491139068/"

# Upewnij się, że katalog istnieje
os.makedirs("docs/exampels", exist_ok=True)

img = qrcode.make(url)
img.save("docs/exampels/qr_meta_horizon.png")
img.show()

print("Plik został zapisany jako 'docs/exampels/qr_meta_horizon.png'")
```

## Funkcje

- ✅ Generowanie kodu QR z dowolnego adresu URL
- ✅ Automatyczne zapisywanie jako plik PNG
- ✅ Wyświetlanie wygenerowanego kodu QR
- ✅ Prosty i szybki w użyciu

## Autor

[mplik](https://github.com/mplik)

## Licencja

MIT License
