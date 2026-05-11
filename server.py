from flask import Flask, render_template
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv() # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.permanent_session_lifetime = timedelta(hours=1)

@app.errorhandler(404)
def not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def internal_error(e):
    # Log the error for internal tracking (vulnerability mitigation)
    app.logger.error(f"Server Error: {e}")
    return render_template('errors/500.html'), 500

@app.after_request
def add_security_headers(response):
    # VULN-17: Proxy Disclosure / Information Leakage
    response.headers['Server'] = 'NovaCorp-Secure-Server'
    response.headers.pop('X-Powered-By', None)

    # Cabeceras de seguridad fundamentales (Clickjacking, etc.)
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # CSP: Permite recursos con SRI de jsdelivr
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "font-src 'self' https://cdn.jsdelivr.net; "
        "img-src 'self' data:; "
        "connect-src 'self';"
    )
    
    return response

