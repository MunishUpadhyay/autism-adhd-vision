# Autism & ADHD Vision-Based Behavior Analysis System

## 📌 Problem Statement
Build a vision-based system to detect behavioral patterns associated with Autism and ADHD using video input.

---

## 📌 System Overview
The pipeline operates as a modular abstraction extracting physical variables completely securely:

**Input (Video/Webcam)** → **MediaPipe Feature Extraction** → **Behavioral Signal Computation** → **Rule-Based Analysis** → **Frontend Visualization**

---

## 📌 Features
- **Video upload analysis**
- **Webcam recording** (temporal 6s looping captures natively mapping continuous behavioral vectors)
- **Real-time behavioral metrics**
- **Explainable outputs** (No black-box ML variables)
- **Clean dashboard UI**

---

## 📌 Tech Stack

**Frontend:**
- React (Vite)
- TailwindCSS (v4)
- Lucide React

**Backend:**
- FastAPI
- OpenCV
- MediaPipe (Python)

---

## 📌 Folder Structure & File Roles

```text
autism-adhd-vision/
│
├── backend/
│   ├── main.py                # FastAPI entry point managing global routing, ports, and CORS policies
│   └── services/
│       └── analyzer.py        # Pipeline bridge cleanly parsing incoming Form-Data payloads and executing the local ML extraction
│
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── Dashboard.jsx    # Complete UI orchestrator routing all secondary metrics into the flex grid structure securely
│       │   ├── VideoInput.jsx   # Massive state machine managing complex Webcam recording hooks alongside native Video Uploads
│       │   ├── ScoreCard.jsx    # The core numerical widget mapping 0->100% metrics across Lucide icons and animated loading bars
│       │   └── IndicatorCard.jsx# Rigid text component cleanly categorizing erratic/repetitive/stable conditions into colored targets
│       │
│       ├── services/
│       │   └── api.js         # Dedicated Axios HTTP wrapper isolating async POST fetch commands sending video Blobs reliably
│       │
│       ├── pages/
│       │   └── Home.jsx       # Foundational wrapper establishing top tier spacing, structural loops, and the "New Analysis" wipe switch
│       │
│       ├── App.jsx            # Default application mapping
│       └── main.jsx           # Vite bootstrapper hooking the React virtual environment over top the physical DOM index
│
├── src/ (The Core Engine)
│   ├── modules/
│   │   ├── pose_module.py       # Scans frame coordinates natively quantifying rigid body movement and absolute positional tracking variance
│   │   ├── eye_gaze_module.py   # Extracts ocular tracking metrics transforming facial focal drops locally into Gaze Stability algorithms
│   │   ├── facial_module.py     # Checks secondary structural dependencies via facial mesh grids
│   │   └── behavior_scoring.py  # The Master Mechanical Engine dynamically reducing spatial arrays backwards into formatted Diagnostic Strings!
│   │
│   ├── utils/
│   │   └── video_processor.py   # High-performance OpenCV handler locking memory caps securely tearing down processing videos safely
│   │
│   └── main.py                  # Local Python CLI debug tool bypassing the entire frontend architecture running pipeline simulations directly
│
├── data/
│   └── raw/                     # Protected filesystem environment utilized primarily as isolated media caching arrays
│
├── README.md                    # Primary repository topology structure explaining overarching component definitions definitively
└── requirements.txt             # Freezes Python backend environmental targets defining Uvicorn, FastAPI, and OpenCV distributions 
```

---

## 📌 How To Run

### Backend API Start:
```bash
# Run this from the root 'autism-adhd-vision' directory
uvicorn backend.main:app --reload
```
*(Server locks to port 8000 handling OpenCV matrices locally)*

### Frontend Client Start:
```bash
cd frontend
npm install
npm run dev
```
*(React application spins up utilizing absolute Tailwind rendering boundaries natively)*

---

## 📌 How It Works
1. User uploads a video or executes a local camera capture directly via the browser.
2. The payload is sent tightly over POST constraints masking natively against the Backend boundary. 
3. OpenCV buffers the video while MediaPipe scans every single frame detecting absolute bounds (pose variance + ocular drift arrays + facial structure targets).
4. The rule engine translates pixel coordinate limits accurately over baseline thresholds mapping safe matrices (e.g., categorizing motion limits > threshold as physically erratic behavior arrays).
5. The extracted arrays snap synchronously back over the network triggering React rendering rules to cascade identically parsing dashboard grids successfully!

---

## 📌 Limitations
- **Depends entirely on lighting and visibility matrices** cleanly parsing tracking limits.
- **Not a medical diagnosis tool.** Strictly an interpretive analysis pipeline handling mechanical variables natively.
- **Dataset-dependent behavior patterns.** Threshold arrays must calibrate accurately mapping across diverse localizations universally perfectly. 

---

## 📌 Future Improvements
- Deep learning integrations mapping long-sequence dependencies securely.
- Multi-person background parsing loops cleanly separating spatial subjects dynamically.
- Real-time zero-latency socket streaming integrations supporting ultra-fast native bounds perfectly!
