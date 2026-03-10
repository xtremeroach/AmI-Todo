# Django SAML Test Site

This is a secure Django web application integrated with Microsoft Entra ID (formerly Azure AD) for Enterprise Single Sign-On (SSO) via SAML 2.0. Standard user authentication is entirely delegated to Entra ID, routing users dynamically to a protected `/todos/` interface based on Role-Based Access Control (RBAC). 

The application has been hardened to securely enforce **OWASP ASVS Level 1** compliance, including strict HTTPS redirectional controls, encrypted session cookie flags, disabled tracebacks, and Subdomain HSTS Preloading capabilities.

---

## 🚀 Features

- **Strict SAML SSO**: Blocks local user logins and generic `/admin/` bypasses.
- **Enterprise Provisioning**: Auto-creates returning SSO IDP users directly on the internal database.
- **Role-Based Access Control (RBAC)**: Includes separated `Reader` (View-Only) and `Writer` (Create/Update) groups mapped directly to frontend features.
- **ASVS Level 1 Compliance**: Out-of-the-box hardened deployment configurations.
- **Isolated Secrets Management**: Centralized environment variable integrations.

---

## 🛠 Prerequisites

Before you begin, ensure you have the following installed:
1. **Python 3.10+**
2. **Git**

---

## 📦 Installation Instructions

### 🐧 Linux / macOS

1. **Clone the repository:**
   ```bash
   git clone https://github.com/xtremeroach/AmI-Todo.git
   cd AmI-Todo
   ```

2. **Set up the virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Python dependencies:**
   ```bash
   python3 -m pip install --upgrade pip
   pip install Django django-saml2-auth pysaml2 python-dotenv
   ```

### 🪟 Windows

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/xtremeroach/AmI-Todo.git
   cd AmI-Todo
   ```

2. **Set up the virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install Python dependencies:**
   ```powershell
   python -m pip install --upgrade pip
   pip install Django django-saml2-auth pysaml2 python-dotenv
   ```


---

## ⚙ Configurations

1. **Environment Variables**:
   In the root directory, create a `.env` file containing your secret credentials and deployment flags:
   ```env
   # Django Secrets
   DJANGO_SECRET_KEY=your-long-cryptographically-secure-key-here
   DJANGO_DEBUG=False
   ENFORCE_HTTPS=True
   
   # SAML Federation
   SAML2_METADATA_URL="https://login.microsoftonline.com/<your-tenant-id>/federationmetadata/2007-06/federationmetadata.xml?appid=<your-app-id>"
   ```
   *(Note: You can also place these configurations inside `venv/.env`.)*

2. **SAML Certificates**:
   Place your Identity Provider metadata file (e.g., `Federation_File.xml`) and Base64 encoded verification certificates (e.g., `Federation_Cert.cer`) into the project directory and set the paths in your `.env` file via `SAML2_METADATA_LOCAL_FILE_PATH` and `SAML2_CERT_FILE`.



---

## 🗄 Database Initialization

1. Run the Django migrations to construct the SQLite schema:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. If custom base configurations are needed, run the setup macro:
   ```bash
   python setup_db.py
   ```

---

## 🚦 Running the Application

Once dependencies and environment files are correctly prepared, start the backend server!

```bash
python manage.py runserver
```

1. Open your browser and navigate to `http://127.0.0.1:8000/`.
2. The user will be seamlessly bounced out to Microsoft Entra for SSO Federation authentication.
3. Upon returning locally with a `POST`, they will arrive instantly within the `/todos/` frontend framework.
