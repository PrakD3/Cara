# CARA — Technical Guide & Architecture

This document outlines the stabilized architecture for the **Contextual Adherence & Recovery Architecture (CARA)** ecosystem.

---

## 🛠 1. Tech Stack

### **Mobile (apps/mobile)**
*   **Framework**: Expo SDK 54 (SDK 54 provides the most stable native bindings for React Native 0.81).
*   **Core**: React Native 0.81 + React 19.1.0.
*   **Styling**: 
    *   **NativeWind 4.2.1**: Used for Tailwind-based utility classes.
    *   **Standard Styles**: Used for high-fidelity components (Shadows, Glassmorphism) to ensure runtime stability on Windows/iOS.
*   **Icons**: Lucide React Native (Premium thin-stroke icons).
*   **Networking**: Native Fetch API with auto-retry and Mock Data fallback.

### **Backend (apps/api)**
*   **Framework**: FastAPI (Python 3.12+).
*   **Web Server**: Uvicorn with `--host 0.0.0.0` (Enabled for cross-device Wi-Fi connectivity).
*   **Database**: SQLAlchemy 2.0 with SQLite (Local Development).
*   **Validation**: Pydantic v2 (Strict typing).

### **Web Dashboard (apps/web)**
*   **Framework**: Next.js 15+ (App Router).
*   **Styling**: Tailwind CSS + Shadcn UI.

---

## 🌐 2. Networking Architecture (Critical)

For the Mobile App (iPhone) to talk to the Laptop (FastAPI), we use a **Local Network Bridge**:

1.  **Server IP**: The backend must listen on `0.0.0.0` (all interfaces) instead of `127.0.0.1`.
2.  **Port 8080**: We moved from 8000 to 8080 to avoid Windows internal service conflicts.
3.  **Firewall**: Port 8080 is explicitly opened in the Windows Advanced Firewall to allow incoming iPhone requests.
4.  **Static IP**: The `API_URL` in `App.tsx` is set to your Hotspot IP (`192.168.137.1`).

---

## 🚀 3. How to Run

### **Step 1: Start the Backend**
Open a terminal and run:
```powershell
cd apps/api
.\.venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

### **Step 2: Start the Mobile App**
Open a **new** terminal and run:
```powershell
cd apps/mobile
npx expo start --clear
```
*Scan the QR code with your iPhone camera to open in **Expo Go**.*

### **Step 3: Start the Web Dashboard**
Open a **third** terminal and run:
```powershell
pnpm --filter web dev
```

---

## 🏗 4. Development Workflow

1.  **Monorepo Management**: Use `pnpm` from the root. To install a new package for mobile, use `pnpm add <pkg> --filter mobile`.
2.  **Windows Stability**: We use `.npmrc` with `shamefully-hoist=true` to ensure Metro can find nested dependencies.
3.  **Babel Config**: We use the `presets` array in `babel.config.js` for NativeWind v4, which is the "Golden Rule" for Expo 54 on Windows.
4.  **Graceful Degradation**: If the backend is offline, the app automatically switches to **Mock Data Mode**, allowing UI testing without a server connection.

---

## 🐼 5. Dosi Mascot Integration
The "Dosi" Assistant (Panda) is the core of the UX. It is implemented as a data-driven card that consumes the `patient/me` endpoint. It provides contextual health advice based on the patient's real-time adherence logs.
