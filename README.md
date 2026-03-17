# QR Code Generator

Prosty generator kodów QR w języku Python, który tworzy kod QR z podanego adresu URL.

## 🌟 Live Demo

**Wypróbuj aplikację online (bez instalacji!):**

🔗 **[https://web-production-18f06.up.railway.app](https://web-production-18f06.up.railway.app)**

Aplikacja działa 24/7 w chmurze Railway. Wejdź, wpisz URL, wygeneruj QR i pobierz PNG - wszystko w przeglądarce! 🚀

---

## Opis

Skrypt generuje kod QR na podstawie wprowadzonego adresu URL i zapisuje go jako plik PNG. Kod QR można następnie zeskanować telefonem, aby szybko przejść do zapisanego adresu.

## 🚀 Sposoby użycia

Projekt oferuje **3 sposoby** generowania kodów QR:

### 1. 🌐 Flask Web App (Polecane!)
- **Nowoczesny interfejs webowy**
- Dostępny w przeglądarce
- Bez edycji kodu - wszystko przez formularz
- Możliwość hostingu online (Railway/Render)
- Idealne dla użytkowników bez znajomości Pythona

### 2. 🔧 Zaawansowany skrypt (qr_generator_v2.py)
- Generowanie QR z niestandardowym podpisem
- Edycja parametrów w kodzie
- Automatyczne zapisywanie w `outputs/`

### 3. ⚡ Prosty skrypt (qr_kod.py)
- Podstawowe funkcje
- Najprostsze użycie
- Szybkie generowanie bez dodatków

---

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
pip install -r requirements.txt
```

lub w środowisku wirtualnym:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac
pip install -r requirements.txt
```

---

## 🌐 Flask Web App - Użycie

### Uruchomienie lokalne

1. Upewnij się, że zainstalowałeś wszystkie zależności:
```bash
pip install -r requirements.txt
```

2. Uruchom serwer Flask:
```bash
python app.py
```

3. Otwórz przeglądarkę i wejdź na:
```
http://127.0.0.1:5000
```

4. **Gotowe!** 🎉
   - Wpisz URL w formularzu
   - Dodaj opcjonalną etykietę
   - Kliknij "Generuj kod QR"
   - Pobierz wygenerowany PNG

### Hosting online (Railway/Render)

#### Railway (Darmowy)

1. Załóż konto na [railway.app](https://railway.app)
2. Zaloguj się przez GitHub
3. Kliknij **"New Project"** → **"Deploy from GitHub repo"**
4. Wybierz `mplik/qr-code-generator`
5. Railway automatycznie:
   - Wykryje Python
   - Zainstaluje dependencies z `requirements.txt`
   - Uruchomi aplikację zgodnie z `Procfile`
6. **Gotowe!** Otrzymasz link do działającej aplikacji

#### Render (Darmowy)

1. Załóż konto na [render.com](https://render.com)
2. Połącz z GitHubem
3. Utwórz **"New Web Service"**
4. Wybierz repozytorium `qr-code-generator`
5. Render automatycznie skonfiguruje deployment
6. **Gotowe!** Twoja aplikacja jest online

### Funkcje Web App

- ✅ Intuicyjny interfejs użytkownika
- ✅ Generowanie QR w czasie rzeczywistym
- ✅ Niestandardowe etykiety pod kodem QR
- ✅ Pobieranie PNG jednym kliknięciem
- ✅ Responsywny design (działa na telefonach)
- ✅ Profesjonalny wygląd z gradientowym tłem
- ✅ Brak potrzeby edycji kodu

---

## ⚡ Użycie skryptów CLI

1. Edytuj plik `qr_kod.py` i wpisz swój adres URL w zmiennej `url`:
```python
url = "https://twoj-adres.com"
```

2. Uruchom skrypt:
```bash
python qr_kod.py
```

3. Kod QR zostanie zapisany w katalogu `docs/examples/qr_meta_horizon.png` i automatycznie otworzy się w domyślnej przeglądarce obrazów.

---

## Przykład

![Przykładowy kod QR dla QR app generator](static/qr-app-generator.png)

*Przykładowy kod QR wygenerowany dla "QR app generator"*

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
