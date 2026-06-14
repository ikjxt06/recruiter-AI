# Render Backend Deployment

This repo includes `render.yaml`, so Render can create the FastAPI web service from the GitHub repository.

For a no-payment setup, use Neon Free Postgres for the database and paste the Neon connection string into Render as `DATABASE_URL`.

## Steps

1. Push this repository to GitHub.
2. Open Render Dashboard.
3. Choose **New > Blueprint**.
4. Connect the GitHub repository.
5. Select this repo and apply the blueprint.
6. Render will ask for `DATABASE_URL` and `ALLOWED_ORIGINS`.
7. Use a Neon Free Postgres connection string for `DATABASE_URL`.
8. Use your Vercel frontend URL for `ALLOWED_ORIGINS`.
9. After deploy, open the backend URL:

```text
https://YOUR_RENDER_SERVICE.onrender.com/docs
```

## Required Environment Update

After your Vercel frontend is live, update the Render service environment variable:

```env
ALLOWED_ORIGINS=https://YOUR_VERCEL_APP.vercel.app
```

If you also test locally, use both origins separated by commas:

```env
ALLOWED_ORIGINS=https://YOUR_VERCEL_APP.vercel.app,http://localhost:5173,http://127.0.0.1:5173
```

Then redeploy/restart the Render service.

## Free Neon Database

1. Go to Neon and create a free Postgres project.
2. Copy the pooled connection string.
3. In Render, set:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST.neon.tech/DBNAME?sslmode=require
```

The backend converts this to the SQLAlchemy `psycopg` driver internally.

## Vercel Frontend Setting

In Vercel, set this environment variable:

```env
VITE_API_URL=https://YOUR_RENDER_SERVICE.onrender.com/api/v1
```

Redeploy the frontend after changing it.

## Notes

- Render runs `alembic upgrade head` before starting the API.
- The deployment uses `requirements-lite.txt` to avoid native ChromaDB build issues.
- Uploaded resumes are stored on the service filesystem, which is not ideal for production. Use S3, Cloudinary, or another object store for long-term resume storage.
