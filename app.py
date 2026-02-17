import os
from flask import Flask, render_template, request, send_file, session, redirect, url_for
from flask_session import Session
from dotenv import load_dotenv
import stripe
import qrcode
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


# Wczytaj zmienne środowiskowe z pliku .env
load_dotenv()

app = Flask(__name__)

# Konfiguracja Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret')
Session(app)

# Klucze Stripe z .env
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
STRIPE_PRICE_ID = os.environ.get('STRIPE_PRICE_ID')

stripe.api_key = STRIPE_SECRET_KEY
@app.route('/checkout', methods=['POST'])
def checkout():
    """Endpoint do utworzenia sesji Stripe Checkout i przekierowania do płatności"""
    try:
        session_stripe = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': STRIPE_PRICE_ID,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=url_for('success', _external=True),
            cancel_url=url_for('paywall', _external=True)
        )
        return redirect(session_stripe.url)
    except Exception as e:
        return render_template('paywall.html', error=f'Błąd Stripe: {str(e)}')

@app.route('/success')
def success():
    """Strona po udanej płatności"""
    # Aktywuj subskrypcję w sesji użytkownika
    session['subscription_active'] = True
    return render_template('success.html')

@app.route('/paywall')
def paywall():
    """Strona paywalla (limit darmowych kodów QR)"""
    return render_template('paywall.html')

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
    
    # Licznik darmowych kodów QR w sesji
    qr_count = session.get('qr_count', 0)
    subscription_active = session.get('subscription_active', False)

    # Limit 3 darmowe kody QR, potem paywall
    if qr_count >= 3 and not subscription_active:
        return render_template('paywall.html')

    # Generuj unikalną nazwę pliku z timestampem
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"qr_{timestamp}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try:
        generate_qr_with_label(url, label, filepath)
        # Zwiększ licznik tylko jeśli nie ma subskrypcji
        if not subscription_active:
            session['qr_count'] = qr_count + 1
        return render_template('index.html', 
                             success=True, 
                             qr_image=f"generated/{filename}",
                             url=url,
                             label=label,
                             qr_count=session.get('qr_count', 0),
                             subscription_active=subscription_active)
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
