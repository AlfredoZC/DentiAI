# 🦷 DentAI - Dental AI Clinic

Web application for detecting oral affections using Artificial Intelligence (YOLOv5).

## 🚀 Features
- **AI Diagnosis:** Detects Caries, Gingivitis, Ulcers, etc.
- **Real-time Analysis:** Use your camera or upload images.
- **Patient History:** Saves all detections per user.
- **Secure Access:** User registration and login.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/DentAI.git
   cd DentAI
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ How to Run

Simply double-click on **`run_app.bat`** file.

Or run manually:
```bash
uvicorn interfaz.main:app --reload
```
Access the app at: `http://127.0.0.1:8000/static/index.html`

## 🧠 Model
The project uses a custom trained YOLOv5 model (`best.pt`) located in `interfaz/best.pt`.

## 👤 Author
Jose Alfredo Zambrana Cruz
