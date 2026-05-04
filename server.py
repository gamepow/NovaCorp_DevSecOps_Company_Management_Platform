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

