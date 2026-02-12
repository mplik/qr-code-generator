import os
from flask import Flask, render_template, request, send_file
import qrcode
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

app = Flask(__name__)

# Ustaw folder na wygenerowane QR kody
UPLOAD_FOLDER = 'static/generated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_qr_with_label(url, label, filename):
    """Generuje kod QR z podpisem (wykorzystuje logikę z qr_generator_v2.py)"""
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
    bbox = draw.textbbox((0, 0), label, font=font)
    szer_napisu = bbox[2] - bbox[0]
    wys_napisu = bbox[3] - bbox[1]
    x = (szerokosc - szer_napisu) // 2
    y = wysokosc + (wysokosc_podpisu - wys_napisu) // 2
    draw.text((x, y), label, font=font, fill='black')
    
    # Zapisywanie
    img_podpis.save(filename)
    return filename

@app.route('/')
def index():
    """Główna strona z formularzem"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Endpoint do generowania QR kodu"""
    url = request.form.get('url', '')
    label = request.form.get('label', 'QR Code')
    
    if not url:
        return render_template('index.html', error="Proszę podać adres URL")
    
    # Generuj unikalną nazwę pliku z timestampem
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"qr_{timestamp}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    try:
        generate_qr_with_label(url, label, filepath)
        return render_template('index.html', 
                             success=True, 
                             qr_image=f"generated/{filename}",
                             url=url,
                             label=label)
    except Exception as e:
        return render_template('index.html', error=f"Błąd podczas generowania: {str(e)}")

@app.route('/download/<filename>')
def download(filename):
    """Endpoint do pobierania wygenerowanego QR kodu"""
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    # Dla Railway/Render - używamy zmiennej środowiskowej PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
