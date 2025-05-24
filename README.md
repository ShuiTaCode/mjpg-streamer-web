# mjpeg-streamer-web

A modern, simple web frontend for multiple MJPEG streams (e.g. from USB cameras) with a Python backend and React frontend.

## Features

- Clear display and switching of multiple cameras
- Live MJPEG stream in the browser
- Automatic detection of all `/dev/video*` devices

---

## Requirements

- Python 3.8+
- Node.js (recommended: 18+)
- npm

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/mjpg-streamer-web.git
cd mjpg-streamer-web
```

### 2. Set up the backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ..
```

### 3. Set up the frontend

```bash
cd frontend
npm install
cd ..
```

---

## Start the application

### Development (both at once)

From the main directory:

```bash
cd frontend
npm run dev
```

- The frontend will run at [http://localhost:3001](http://localhost:3001)
- The backend will run at [http://localhost:8081](http://localhost:8081) (started automatically)

### Production

1. **Build the frontend:**

   ```bash
   cd frontend
   npm run build
   ```

2. **Start the backend:**

   ```bash
   cd ../backend
   source .venv/bin/activate
   PYTHONPATH=src python3 main.py
   ```

---

## Usage

- Open [http://localhost:3001](http://localhost:3001) in your browser.
- Use the dropdown at the top to select the desired camera.
- The live stream will be displayed below.

---

## Directory structure

```
mjpg-streamer-web/
│
├── backend/         # Python backend (HTTP/MJPEG server)
│   └── src/
│       └── mjpg_streamer_web/
│           ├── server.py
│           ├── camera.py
│           └── ...
│
├── frontend/        # React frontend
│   ├── src/
│   └── ...
│
├── index.html       # (Legacy) static example frontend
└── .gitignore
```

---

## Notes

- The backend automatically detects all `/dev/video*` devices (Linux).
- For Windows/Mac, adjustments may be necessary.
- The software is intended for local networks – for internet access, please add authentication and HTTPS!

---

## License

[MIT License](https://opensource.org/licenses/MIT)

---

## Contributing

Pull requests, bug reports, and feature requests are welcome!  
Please open an issue if you find a bug or have an idea.

---

**Enjoy using MJPEG-Streamer Web!** 