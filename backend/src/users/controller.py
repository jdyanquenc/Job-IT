from fastapi import APIRouter, Request, status
from uuid import UUID
from ..rate_limiter import limiter

from ..database.core import DbSession
from . import models
from . import service
from ..auth.service import CurrentUser

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/check-email", response_model=models.EmailAvailabilityResponse)
async def check_email_availability(email: str, db: DbSession):
    return service.is_email_taken(db, email)


@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/hour")
async def register_user(request: Request, db: DbSession, register_user_request: models.RegisterUserRequest):
    service.register_user(db, register_user_request)


@router.get("/me", response_model=models.UserResponse)
def get_current_user(current_user: CurrentUser, db: DbSession):
    return service.get_user_by_id(db, current_user.get_uuid())


@router.put("/change-password", status_code=status.HTTP_200_OK)
def change_password(password_change: models.PasswordChange, db: DbSession, current_user: CurrentUser):
    service.change_password(db, current_user.get_uuid(), password_change)
