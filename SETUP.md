# 🚀 Setting Up CARA for Development

Follow these steps to get the project running on your local machine.

## 📋 Prerequisites
Ensure you have the following installed:
- **Node.js** (v18 or higher)
- **pnpm** (`npm install -g pnpm`)
- **Python** (3.11 or higher)
- **Git**

---

## 🛠️ Initial Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/PrakD3/Cara.git
   cd Cara
   ```

2. **Install Node dependencies & Approve Builds:**
   ```bash
   pnpm install
   pnpm approve-builds
   ```

---

## 🔐 Environment Variables

You need to set up `.env` files for both the Web and API layers.

### Backend (API)
1. Go to `apps/api`
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. **Note on Database**: By default, CARA uses **SQLite** for zero-config local development. You do **not** need to set `DATABASE_URL` unless you are migrating to production.

---

## 🏃‍♂️ Running the Project

### 1. Start the Backend (FastAPI)
```bash
cd apps/api
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```
- **API Docs**: [http://localhost:8080/docs](http://localhost:8080/docs)

### 2. Start the Mobile App (Expo)
```bash
cd apps/mobile
npx expo start --clear
```
- **iPhone Link**: Scan the QR code to open in **Expo Go**.

### 3. Start the Web Dashboard
In a new terminal:
```bash
pnpm --filter web dev
```
- **Dashboard**: [http://localhost:3000](http://localhost:3000)

---

## 🌐 Networking (iPhone Connection)
If your phone cannot see the server, ensure:
1. Your **Firewall** is disabled or allows Port 8080.
2. Your Wi-Fi network profile is set to **Private** (not Public).
3. `API_URL` in `apps/mobile/App.tsx` matches your laptop's IP.

---

## 📦 Tech Stack Ref
- **Web**: Next.js 15+, Tailwind 4, Lucide Icons
- **Mobile**: Expo SDK 54, React Native 0.81
- **Backend**: FastAPI, SQLite (Dev), SQLAlchemy
- **AI**: Groq, Gemini 1.5 Flash
