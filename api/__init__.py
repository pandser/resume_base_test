from fastapi import APIRouter

from api.resumes import router as resume_router
from api.auth import router as auth_router


router = APIRouter()
router.include_router(resume_router)
router.include_router(auth_router)
