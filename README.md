# 👋 SignMeet

SignMeet is a webcam-based application that recognizes a limited set of hand gestures and displays matching sign animations. It uses MediaPipe to detect hand landmarks and a pre-trained Random Forest model to classify gestures. The application also includes speech-based phrase search.

## ✨ Features

- 🔐 User and administrator authentication backed by MySQL
- 📷 Live gesture recognition and gesture data capture
- 🧠 Gesture model training
- 🔎 Phrase search with matching GIF animations
- 🌐 Translation of recognized labels

Recognition is limited to the gestures represented in the supplied training data. Translation requires an internet connection.

## 🧰 Technology

Python, Flask, MySQL, OpenCV, MediaPipe and JavaScript.

## 📁 Project structure

```text
main.py                      Flask routes and application entry point
camera.py                    Live webcam gesture prediction
camera1.py                   Webcam landmark capture for training samples
templates/                   Flask pages
static/                      Browser assets, seeded CSV data, and sign GIFs
gesture_model.pkl            Included trained classifier
gesture_map.pkl              Included model-label mapping
database/sign_meet_new.sql   MySQL tables and sample gesture/image records
tests/                       Local checks for included gesture data and models
DEMO/DEMO.mp4                Existing project demo
DEMO/                         Project report, presentation, and base paper
dd/                           Separate static website files; not served by main.py
sign/                         Legacy PHP VoiceRSS text-to-speech files
```

## 📋 Requirements

- 64-bit Python 3.8
- MySQL server
- Webcam for gesture capture and recognition

## ⚙️ Setup on Windows

Create a virtual environment and install the dependencies:

```powershell
py -3.8 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Create the database and load the included schema:

```powershell
mysql -u root -p -e "CREATE DATABASE sign_meet_new CHARACTER SET utf8;"
Get-Content -Raw .\database\sign_meet_new.sql | mysql -u root -p sign_meet_new
```

Update `.env` with your MySQL settings and a private `FLASK_SECRET_KEY`. Register a user in the application. The schema does not create an administrator account.

## 🚀 Run

Start the application with MySQL running and the database configured:

```powershell
python main.py
```

Open <http://127.0.0.1:5000> in your browser and allow webcam access when prompted.

## 🧪 Tests

```powershell
python -m unittest discover -s tests -v
python -m compileall -q main.py camera.py camera1.py tests
```

The tests validate the included model files and gesture data. They do not require or test MySQL, webcam hardware, or online translation.

## 🎬 Demo

See [DEMO/DEMO.mp4](DEMO/DEMO.mp4).

## ⚠️ Limitations

- SignMeet recognizes only the gestures in its training data and is not a complete sign-language translation system.
- Database features require MySQL. Gesture features require a compatible webcam and dependencies.
- Some legacy routes and the separate PHP files are not part of the current application flow.
