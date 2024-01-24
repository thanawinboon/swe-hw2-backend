from typing import List, Tuple
from datetime import datetime

from sqlmodel import select

from src.models.leave_requests import LeaveRequest, LeaveRequestStatus
from src.services.base import BaseService
from src.services.users import UserService
from src.utils.time_calc import days_between


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

    def get_leave_request_by_id(self, id: int) -> LeaveRequest:
        """
        Gets a leave request with the given id.
        :param id: The id of the leave request to query.
        :return: The leave request with given id.
        """
        query = select(LeaveRequest).where(LeaveRequest.id == id)
        result: LeaveRequest = self.session.exec(query).one()

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
        leave_request = self.get_leave_request_by_id(leave_request_id)
        self.session.delete(leave_request)
        self.session.commit()

    def set_leave_request_status(
        self, leave_request_id: int, status: LeaveRequestStatus
    ) -> None:
        """
        Sets the status of a leave request.
        :param leave_request_id: The id of the leave request to set.
        :param status: The status to set.
        """
        leave_request = self.get_leave_request_by_id(leave_request_id)
        leave_request.status = status
        self.session.add(leave_request)
        self.session.commit()

    def valid_leave_request_date_range(
            self, 
            requester_id: int, 
            requested_date_range: Tuple[datetime]
            ) -> bool:
        """
        Checks if a user can request for leave on a given day.
        :param requester_id: The id of the user to check.
        :param requested_date_range: The date range to check.
        :return: True if the user can request for leave on the given day, False otherwise.
        """
        START_DATE_INDEX = 0
        END_DATE_INDEX = 1
        query = select(LeaveRequest).where(LeaveRequest.requester_id == requester_id)

        for leave_request in self.session.exec(query).all():
            start_date_in_range = leave_request.start_date <= requested_date_range[START_DATE_INDEX] <= leave_request.end_date
            end_date_in_range = leave_request.start_date <= requested_date_range[END_DATE_INDEX] <= leave_request.end_date
            if start_date_in_range:
                return False
            if end_date_in_range:
                return False
        return True
    
    def leave_request_allowed(self, leave_request: LeaveRequest) -> bool:
        """
        Checks if a user can request for leave.
        :param leave_request: The leave request to check.
        :return: True if the user can request for leave, False otherwise.
        """
        date_range = (leave_request.start_date, leave_request.end_date)
        request_date_valid = self.valid_leave_request_date_range(leave_request.requester_id, date_range)

        days_requested: int = days_between(leave_request.start_date, leave_request.end_date)
        user_remaining_leave_days: int = UserService(self.session).get_leave_days_by_user_id(leave_request.requester_id)
        has_enough_leave_days = days_requested <= user_remaining_leave_days

        return request_date_valid and has_enough_leave_days
