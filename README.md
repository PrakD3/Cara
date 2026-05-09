# CARA — Contextual Adherence & Recovery Architecture

A mobile-first medication adherence ecosystem.

## Structure

- `apps/web`: Next.js 16 (latest) frontend dashboard.
- `apps/api`: FastAPI backend.
- `packages/shared-types`: Shared TypeScript types.

## Tech Stack

- **Frontend**: Next.js 16, Tailwind CSS, Lucide Icons, Zustand, TanStack Query.
- **Backend**: FastAPI, SQLAlchemy, Pydantic v2, APScheduler.
- **AI**: Groq (Llama 3) for ultra-fast coaching, Gemini 1.5 Flash.
- **Tooling**: BiomeJS (Linting & Formatting).

## Getting Started

### Prerequisites

- Node.js (Latest)
- pnpm
- Python 3.11+

### Installation

```bash
pnpm install
cd apps/api
pip install -r requirements.txt
```

### Running the App

#### Web
```bash
pnpm --filter web dev
```

#### API
```bash
cd apps/api
uvicorn main:app --reload
```

## Linting & Formatting

We use **BiomeJS**.

```bash
pnpm lint
pnpm format
```
