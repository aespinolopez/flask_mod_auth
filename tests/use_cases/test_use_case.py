from unittest import mock

from app.mod_auth.use_cases import requests_objects as req, response_objects as res
from app.mod_auth.use_cases.use_case import UseCase


def test_use_case_cannot_process_valid_requests():
    valid_request_object = mock.MagicMock()
    valid_request_object.__bool__.return_value = True

    use_case = UseCase()
    response = use_case.execute(valid_request_object)

    assert not response
    assert response.type == res.ResponseFailure.SYSTEM_ERROR
    assert response.message == 'NotImplementedError: process_request() not implemented by UseCase class'


def test_use_case_can_process_invalid_requests_and_returns_response_failure():
    invalid_request_object = req.InvalidRequestObject()
    invalid_request_object.add_error('some_param', 'some_message')

    use_case = UseCase()
    response = use_case.execute(invalid_request_object)

    assert not response
    assert response.type == res.ResponseFailure.PARAMETERS_ERROR
    assert response.message == 'some_param: some_message'


def test_use_case_can_manage_generic_exception_from_process_request():
    use_case = UseCase()

    class TestException(Exception):
        pass

    use_case.process_request = mock.Mock()
    use_case.process_request.side_effect = TestException('some_message')
    response = use_case.execute(mock.Mock)

    assert not response
    assert response.type == res.ResponseFailure.SYSTEM_ERROR
    assert response.message == 'TestException: some_message'
