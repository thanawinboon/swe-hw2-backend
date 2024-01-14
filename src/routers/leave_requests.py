from typing import Annotated, List

from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.database import get_session
from src.models.leave_requests import LeaveRequest
from src.models.users import User
from src.routers.users import get_current_user
from src.schemas.leave_requests import LeaveRequestCreate
from src.services.leave_requests import LeaveRequestService
from src.services.users import UserService
from src.utils.time_calc import days_between

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/api/create-leave-request", tags=["leave-requests"])
async def create_leave_request(
        leave_request_info: LeaveRequestCreate,
        current_user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(get_session),
):
    leave_request: LeaveRequest = LeaveRequest(
        requester_id=current_user.id,
        requester=current_user,
        **leave_request_info.model_dump()
    )
    LeaveRequestService(session).create_leave_request(leave_request=leave_request)

    days_requested: int = days_between(leave_request.start_date, leave_request.end_date)
    UserService(session).deduct_remaining_leave_days(
        username=current_user.username, days=days_requested
    )


@router.get("/api/get-all-leave-requests", tags=["leave-requests"])
async def get_all_leave_requests(
        current_user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(get_session),
):
    leave_requests: List[LeaveRequest] = LeaveRequestService(
        session
    ).get_all_leave_requests()
    return leave_requests


@router.delete("/api/delete-leave-request/{leave_request_id}", tags=["leave-requests"])
async def delete_leave_request(
        leave_request_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(get_session),
):
    LeaveRequestService(session).delete_leave_request(leave_request_id)
