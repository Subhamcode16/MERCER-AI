import logging
from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import AuthenticatedUser, get_current_user
from app.database import get_db
from app.models.generation import JobResponse, JobStatus

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/{job_id}", response_model=JobResponse, summary="Poll job status")
async def get_job_status(
    job_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
):
    db = get_db()
    job = await db.jobs.find_one({"_id": job_id, "user_id": user.user_id})
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
        
    return JobResponse(
        job_id=job_id,
        status=JobStatus(job["status"]),
        image_base64=job.get("image_base64"),
        error=job.get("error")
    )
