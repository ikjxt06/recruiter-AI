# TalentIQ AI

Full-stack AI recruitment assistant for bulk resume parsing, candidate ranking, recruiter analytics, and AI-assisted screening.

## Stack

- Frontend: React, Tailwind CSS, Axios
- Backend: FastAPI, SQLAlchemy, PostgreSQL
- AI/NLP: Sentence Transformers, Gemini, LangChain-ready service layer, ChromaDB
- File processing: PyMuPDF, python-docx, pandas

## Repository Structure

```text
backend/
  app/
    api/
    core/
    db/
    models/
    schemas/
    services/
    workers/
  alembic/
frontend/
  src/
    api/
    components/
    pages/
    types/
infra/
docs/
```

## Quick Start

1. Copy environment files:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

2. Start PostgreSQL and ChromaDB dependencies:

```bash
docker compose -f infra/docker-compose.yml up -d
```

3. Start the backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

4. Start the frontend:

```bash
cd frontend
npm install
npm run dev
```

## Main Capabilities

- HR authentication with JWT
- Bulk PDF/DOCX resume upload
- Text extraction and structured candidate parsing
- JD analysis and skill extraction
- Weighted ranking engine
- AI summaries, hiring recommendations, ATS suggestions, interview questions
- Fake experience suspicion scoring
- Candidate comparison
- Recruiter chatbot backed by semantic search
- Analytics dashboard and CSV report export

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for production deployment notes.
