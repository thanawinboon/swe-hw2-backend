from typing import List

from sqlmodel import select

from src.models.leave_requests import LeaveRequest
from src.services.base import BaseService


class LeaveRequestService(BaseService):
    def create_leave_request(self, leave_request: LeaveRequest) -> None:
        """
        Inserts a new leave request into the database.
        :param leave_request: The leave request object containing the user information.
        """
        self.session.add(leave_request)
        self.session.commit()

    def get_leave_requests_by_requester_id(
        self, requester_id: int
    ) -> List[LeaveRequest]:
        """
        Gets all leave requests for user with the given id.
        :param requester_id: The id of the user to get the leave requests for.
        :return: A list of leave requests for the given id.
        """
        query = select(LeaveRequest).where(LeaveRequest.requester_id == requester_id)
        result: List[LeaveRequest] = self.session.exec(query).all()

        return result

    def get_all_leave_requests(self) -> List[LeaveRequest]:
        """
        Fetches all leave requests created.
        :return: A list of all leave requests ordered by start date.
        """
        query = select(LeaveRequest)
        result: List[LeaveRequest] = self.session.exec(query).all()

        return result

    def delete_leave_request(self, leave_request_id: int) -> None:
        """
        Deletes a leave request.
        :param leave_request_id: The id of the leave request to delete.
        """
        query = select(LeaveRequest).where(LeaveRequest.id == leave_request_id)
        result = self.session.exec(query).one()
        self.session.delete(result)
        self.session.commit()
