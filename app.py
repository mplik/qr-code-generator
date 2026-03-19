import os
import threading
from collections import OrderedDict
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

# Limit darmowych kodów QR
FREE_QR_LIMIT = 3

# Maksymalna liczba śledzonych adresów IP (ogranicza zużycie pamięci)
_MAX_TRACKED_IPS = 100_000

# Słownik przechowujący liczbę wygenerowanych kodów QR per adres IP.
# OrderedDict umożliwia usuwanie najstarszych wpisów (LRU) gdy słownik jest pełny.
# Klucz: adres IP, wartość: liczba wygenerowanych kodów QR.
_ip_qr_counts: OrderedDict[str, int] = OrderedDict()
_ip_qr_lock = threading.Lock()


def get_client_ip() -> str:
    """Zwraca adres IP klienta.

    Na platformach Railway/Render ruch przechodzi przez zaufane proxy,
    które dodaje rzeczywisty adres klienta jako ostatni wpis w nagłówku
    X-Forwarded-For.  Pobieramy ten ostatni wpis, aby uniknąć możliwości
    sfałszowania nagłówka przez klienta.
    Gdy nagłówek nie jest dostępny, używamy request.remote_addr.
    """
    forwarded_for = request.headers.get('X-Forwarded-For', '').strip()
    if forwarded_for:
        # Ostatni wpis dodany przez zaufane proxy – niemodyfikowalny przez klienta
        return forwarded_for.split(',')[-1].strip()
    return request.remote_addr or '127.0.0.1'


def _check_and_increment_ip(ip: str) -> tuple[bool, int]:
    """Atomically checks the free-code limit and increments the counter if allowed.

    Returns a (allowed, new_count) tuple.  The entire operation is performed
    inside a single lock acquisition so concurrent requests cannot race past
    the limit check.
    """
    with _ip_qr_lock:
        count = _ip_qr_counts.get(ip, 0)
        if count >= FREE_QR_LIMIT:
            return False, count
        count += 1
        _ip_qr_counts[ip] = count
        _ip_qr_counts.move_to_end(ip)
        # Evict the oldest entry when the dictionary is at capacity
        if len(_ip_qr_counts) > _MAX_TRACKED_IPS:
            _ip_qr_counts.popitem(last=False)
        return True, count

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

    subscription_active = session.get('subscription_active', False)

    # Check the per-IP free limit – enforced even in incognito / private browsing
    client_ip = get_client_ip()

    if not subscription_active:
        allowed, new_count = _check_and_increment_ip(client_ip)
        if not allowed:
            return render_template('paywall.html')
    else:
        new_count = 0

    # Generate a unique filename using a timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"qr_{timestamp}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try:
        generate_qr_with_label(url, label, filepath)
        return render_template('index.html',
                             success=True,
                             qr_image=f"generated/{filename}",
                             url=url,
                             label=label,
                             qr_count=new_count,
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
