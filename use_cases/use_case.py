from app.mod_auth.use_cases.response_objects import ResponseFailure, ResponseSuccess


class UseCase:

    def execute(self, request_object):
        if not request_object:
            return ResponseFailure.build_from_invalid_request_object(request_object)

        try:
            return self.process_request(request_object)
        except Exception as err:
            # todo automate this format from exception
            return ResponseFailure.build_system_error("{}: {}".format(err.__class__.__name__, "{}".format(err)))

    def process_request(self, request_object):
        raise NotImplementedError('process_request() not implemented by UseCase class')
