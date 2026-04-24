from server import app
from routes import auth, companies, companies_admin, users_admin, profile

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)