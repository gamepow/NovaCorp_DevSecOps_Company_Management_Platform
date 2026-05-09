# NovaCorp - DevSecOps - Company Management Platform

**NovaCorp Platform** is an internal web application for managing companies and their associated comments. It supports three roles (`admin`, `owner`, `user`) with different access levels.

---

## 🚀 Live Deployment
The application is deployed on Render:
[**NovaCorp Platform**](https://novacorp-devsecops-company-management.onrender.com)

---

## 👥 Team Members
- **Daniel Carvajal Boza**
- **Duvan Rene Latorre Zapata**
- **Renato Agustín Montenegro Palma**

---

## 🛠️ Deployment and Installation

> [!IMPORTANT]
> All the commands listed below must be executed from the root directory of the project.

### Option 1: Local Deployment (using Virtual Environment)

1.  **Create and activate a virtual environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**:
    Create a `.env` file in the root directory. You can use the following command to generate a secure secret key:
    ```bash
    echo "FLASK_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" > .env
    ```

4.  **Run the application**:
    ```bash
    python3 main.py
    ```
    Visit: `http://localhost:5000`

---

### Option 2: Docker Deployment

1.  **Build the Docker image**:
    ```bash
    docker build -t novacorp-app .
    ```

2.  **Run the container**:
    Ensure you have your `.env` file created (see step 3 above), then run:
    ```bash
    docker run -p 5000:5000 --env-file .env novacorp-app
    ```
    Visit: `http://localhost:5000`

> [!NOTE]
> The database is automatically initialized on the first run of the application.

---

## Default Users

| Username | Password   | Role   | Notes                      |
|----------|------------|--------|----------------------------|
| `alice`  | password1  | user   | Standard employee          |
| `bob`    | password2  | owner  | Owns "Insegura Corp"       |
| `admin`  | admin123   | admin  | Full access                |

---

## Project Structure

```
.
├── main.py                 # Entry point
├── server.py               # Flask app configuration
├── Dockerfile              # Docker container configuration
├── db/
│   └── __init__.py         # Database initialization and helpers
├── routes/
│   ├── auth.py             # Login/logout
│   ├── companies.py        # Company views, dashboard, search
│   ├── companies_admin.py  # Admin company management
│   ├── users_admin.py      # Admin user management
│   └── profile.py          # User profiles
├── templates/
│   ├── base.html           # Shared layout
│   ├── dashboard.html      # Main dashboard
│   ├── auth/               # Login page
│   ├── companies/          # Company pages
│   ├── admin/              # Admin panels
│   ├── profile/            # User profile pages
│   └── errors/             # 404, 403 pages
├── static/
│   └── css/style.css       # Custom styles
├── .gitignore              # Git ignore rules
├── init_db.py              # Manual database setup script
├── LICENSE.md              # Project license
└── requirements.txt        # Python dependencies
```

---

## Technologies

- Python 3 + Flask
- SQLite
- Bootstrap 5.3
- Jinja2 + Bootstrap Icons
- Docker
