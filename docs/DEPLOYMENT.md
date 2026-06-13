# TalentIQ AI Deployment Guide

## Backend

1. Provision PostgreSQL 16.
2. Set production environment variables from `backend/.env.example`.
3. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

4. Run migrations:

```bash
cd backend
alembic upgrade head
```

5. Start FastAPI behind a process manager:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

For production, run multiple workers with Gunicorn/Uvicorn workers and place Nginx or a managed load balancer in front.

## Frontend

```bash
cd frontend
npm ci
npm run build
```

Deploy `frontend/dist` to Vercel, Netlify, S3/CloudFront, Nginx, or any static hosting provider. Set `VITE_API_URL` to the public backend URL before building.

## AI Configuration

- Set `GEMINI_API_KEY` for production AI summaries.
- ChromaDB persists locally at `CHROMA_PATH`; mount this path to persistent storage.
- The sentence-transformer model downloads on first use, so pre-warm the container during deployment.

## Scaling Notes

- For 500+ resume batches, move parsing to a queue such as Celery, RQ, or Dramatiq.
- Store uploaded files in object storage such as S3, Azure Blob Storage, or GCS.
- Add PostgreSQL indexes for high-volume filters on status, created date, email, and ranking score.
- Run vector search on a dedicated Chroma service or managed vector database when concurrent recruiter usage grows.

## Security Checklist

- Use a long random `SECRET_KEY`.
- Enforce HTTPS.
- Restrict CORS to production domains.
- Store API keys in a secrets manager.
- Add rate limits for upload and AI endpoints.
- Scan uploads and enforce max file size.
