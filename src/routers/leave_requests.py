from typing import Annotated, List

from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from src.database import get_session
from src.models.leave_requests import LeaveRequest, LeaveRequestStatus
from src.models.users import User
from src.routers.users import get_current_user
from src.schemas.leave_requests import LeaveRequestCreate
from src.services.leave_requests import LeaveRequestService
from src.services.users import UserService
from src.utils.time_calc import days_between

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/api/create-leave-request", tags=["leave-requests"], response_model=LeaveRequest)
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

    return LeaveRequestService(session).get_leave_request_by_id(leave_request.id)


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
    leave_request: LeaveRequest = LeaveRequestService(session).get_leave_request_by_id(leave_request_id)
    leave_days: int = days_between(leave_request.start_date, leave_request.end_date)
    UserService(session).increment_remaining_leave_days(leave_days)
    LeaveRequestService(session).delete_leave_request(leave_request_id)


@router.put("/api/approve-leave-request/{leave_request_id}", tags=["leave-requests"])
async def approve_leave_request(
        leave_request_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(get_session),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sussy activity detected.",
        )

    LeaveRequestService(session).set_leave_request_status(leave_request_id, LeaveRequestStatus.approved)


@router.put("/api/deny-leave-request/{leave_request_id}", tags=["leave-requests"])
async def approve_leave_request(
        leave_request_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(get_session),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sussy activity detected.",
        )

    LeaveRequestService(session).set_leave_request_status(leave_request_id, LeaveRequestStatus.denied)
