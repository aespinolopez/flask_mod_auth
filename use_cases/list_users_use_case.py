from app.mod_auth.use_cases.response_objects import ResponseSuccess, ResponseFailure


class ListUsersUseCase:

    def __init__(self, repository):
        self.repository = repository

    def execute(self, request_object):
        if not request_object:
            return ResponseFailure.build_from_invalid_request_object(request_object)

        try:
            users = self.repository.list(filters=request_object.filters)
        except Exception as err:
            return ResponseFailure.build_system_error("{}: {}".format(err.__class__.__name__, "{}".format(err)))

        return ResponseSuccess(users)
