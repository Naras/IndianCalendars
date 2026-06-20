# AstroCalendar: Indian Calendars & Panchanga

A modern, high-precision web application to analyze, visualize, and animate Indian calendar cycles and compute Vedic astrological data (Panchanga).

---

## 🌌 Features
1. **Calendar Wheel Gears**: Interactive circular time cycles representing months, seasons, moon phases (tithis), zodiac signs (rashis), and days (vaaras). Supports concentric, static, and synced gear layout views.
2. **Panchanga Calculator**: High-precision offline computations ofLagnas (Ascendants), Moon Signs, Nakshatras, Tithis, Yogas, Karanas, and Vaaras.
3. **Fine-Tuning Controls**: Easily increment or decrement birth years, months, days, hours, and minutes with automatic real-time updates.
4. **Multilingual Script Support**: Instantly transliterates astrological terms to Devanagari, Kannada, IAST, or ITRANS.

---

## 🏗️ Architecture
- **Backend API**: Built with **FastAPI** (Python 3.12+).
- **Astrology Engine**: High-precision calculations powered by the offline `jyotishganit` engine.
- **Frontend client**: Built with Vanilla JS, CSS Glassmorphism, and **D3.js** for visual canvas rendering, bundled using **Vite**.
- **Containerization**: Single container serving both frontend assets (via **Nginx**) and API requests (via **Uvicorn**).

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Node.js 20+
- Docker (optional)

### 1. Backend Setup & Run
Create the virtual environment, install the sanitized requirements list, and run the API server:
```bash
# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI backend (defaults to port 8000)
python backend/main.py
```

### 2. Frontend Setup & Run
Install npm packages and run the Vite bundler on port 5188 (configured to avoid local port conflicts):
```bash
cd frontend
npm install

# Start Vite dev server on port 5188
npx vite --port 5188
```
Open [http://localhost:5188](http://localhost:5188) in your browser.

---

## 🧪 Testing

### Backend Unit Tests
Execute the backend tests covering transliterations, calendar calculations, and API endpoint handlers:
```bash
python -m unittest tests/test_backend.py
```

### Frontend E2E & Integration Tests
Execute the Playwright E2E tests checking page rendering, tab switches, fine-tuning buttons, and network mocks:
```bash
cd frontend
# Ensure Playwright browser binary is installed
npx playwright install chromium

# Run the test suite
npx playwright test
```

---

## 🐳 Docker Deployment

The application compiles the static frontend bundle and wraps both Nginx and the Python API server into a single container. Testing artifacts, logs, and development files are excluded via `.dockerignore`.

```bash
# Build the Docker image
docker build -t indiancalendars .

# Run the container (maps Docker port 80 to host port 8080)
docker run -d -p 8080:80 --name astrocalendar indiancalendars
```
The application will be served at [http://localhost:8080/indiancalendars/](http://localhost:8080/indiancalendars/).
