from app.mod_auth.use_cases.use_case import UseCase
from app.mod_auth.use_cases.response_objects import ResponseSuccess


class ListUsersUseCase(UseCase):

    def __init__(self, repository):
        self.repository = repository

    def process_request(self, request_object):
        users = self.repository.list(filters=request_object.filters)
        return ResponseSuccess(users)
