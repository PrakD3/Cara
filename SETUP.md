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

2. **Install Node dependencies:**
   ```bash
   pnpm install
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
3. Fill in the following keys in `.env`:
   - `GROQ_API_KEY`: Get from [Groq Console](https://console.groq.com/)
   - `DATABASE_URL`: Your PostgreSQL/Supabase link
   - `REDIS_URL`: Your local Redis or Upstash link

### Frontend (Web)
1. Go to `apps/web`
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

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
uvicorn main:app --reload
```
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Start the Frontend (Next.js 16)
In a new terminal (root directory):
```bash
pnpm --filter web dev
```
- **Dashboard**: [http://localhost:3000/dashboard](http://localhost:3000/dashboard)

---

## 🎨 Code Style & Quality
We use **BiomeJS** for linting and formatting. Please run these before pushing:

- **Check for issues:** `pnpm lint`
- **Auto-fix formatting:** `pnpm format`

---

## 📦 Tech Stack Ref
- **Web**: Next.js 16, Tailwind 4, Lucide Icons
- **Backend**: FastAPI, SQLAlchemy, Pydantic v2
- **AI**: Groq (Llama 4 Scout), Gemini 1.5 Flash
- **Cache**: Redis
