from fastapi import APIRouter
from fastapi import Depends

from app.api.deps import get_current_user
from app.api.routes import analytics, auth, candidates, jobs, reports

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
protected = [Depends(get_current_user)]
api_router.include_router(candidates.router, prefix="/candidates", tags=["candidates"], dependencies=protected)
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"], dependencies=protected)
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"], dependencies=protected)
api_router.include_router(reports.router, prefix="/reports", tags=["reports"], dependencies=protected)
