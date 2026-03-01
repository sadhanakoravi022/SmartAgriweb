# SmartAgriWeb

Agricultural management dashboard with water irrigation, crop management, analytics, and inventory tracking.

## Project Structure

```
SmartAgriWeb/
├── app.py                 # Flask application entry point
├── requirements.txt       # Python dependencies
├── README.md
├── templates/             # Jinja2 HTML templates
│   ├── base.html          # Base layout with sidebar
│   ├── auth/
│   │   ├── base_auth.html # Auth pages layout
│   │   ├── login.html     # Login page
│   │   └── signup.html    # Sign up page
│   └── dashboard/
│       ├── home.html      # Home dashboard
│       ├── crop.html      # Crop field management
│       ├── water.html     # Water irrigation
│       ├── analytics.html # Analytics
│       └── inventory.html # Inventory
└── static/                # Static assets
    └── css/
        ├── main.css       # Dashboard styles
        └── auth.css       # Login/Signup styles
```

## Setup & Run

1. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate    # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the app:** Open http://127.0.0.1:5000 in your browser.

## Default Login

- **Username:** admin  
- **Password:** admin123  

## Routes

| Route | Description |
|-------|-------------|
| `/` or `/home` | Home dashboard |
| `/login` | Login page |
| `/signup` | Sign up page |
| `/logout` | Logout |
| `/crop` | Crop field management |
| `/water` | Water irrigation |
| `/analytics` | Analytics |
| `/inventory` | Inventory |
