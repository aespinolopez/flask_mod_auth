import pytest

from app.mod_auth.use_cases.response_objects import ResponseSuccess, ResponseFailure
from app.mod_auth.use_cases import requests_objects as requests


@pytest.fixture
def response_value():
    return {'key': ['value1', 'value2']}


@pytest.fixture
def response_type():
    return 'ResponseError'


@pytest.fixture
def response_message():
    return 'This is a response error'


def test_response_success_is_true():
    assert bool(ResponseSuccess()) is True


def test_response_failure_is_false(response_type, response_message):
    assert bool(ResponseFailure(response_type, response_message)) is False


def test_response_success_contains_value(response_value):
    response = ResponseSuccess(response_value)

    assert response.value == response_value


def test_response_failure_has_type_and_message(response_type, response_message):
    response = ResponseFailure(response_type, response_message)

    assert response.type == response_type
    assert response.message == response_message


def test_response_failure_contains_value(response_type, response_message):
    response = ResponseFailure(response_type, response_message)

    assert response.value == {'type': response_type, 'message': response.message}


def test_response_failure_initialization_with_exception():
    exception = Exception('Just an error message')
    response = ResponseFailure(response_type, exception)

    assert bool(response) is False
    assert response.type == response_type
    assert response.message == '{}: {}'.format(exception.__class__.__name__, '{}'.format(exception))


def test_response_failure_from_invalid_request_object():
    response = ResponseFailure.build_from_invalid_request_object(requests.InvalidRequestObject())

    assert bool(response) is False


def test_response_failure_from_invaild_request_object_with_errors():
    request = requests.InvalidRequestObject()
    request.add_error('path', 'Is mandatory')
    request.add_error('path', 'can\'t be blank')

    response = ResponseFailure.build_from_invalid_request_object(request)

    assert bool(response) is False
    assert response.type == ResponseFailure.PARAMETERS_ERROR
    assert response.message == "path: Is mandatory\npath: can't be blank"


def test_reponse_failure_build_resource_error():
    message = 'test message'
    response = ResponseFailure.build_resource_error(message)

    assert bool(response) is False
    assert response.type == ResponseFailure.RESOURCE_ERROR
    assert response.message == message


def test_reponse_failure_build_parameters_error():
    message = 'test message'
    response = ResponseFailure.build_parameters_error(message)

    assert bool(response) is False
    assert response.type == ResponseFailure.PARAMETERS_ERROR
    assert response.message == message


def test_reponse_failure_build_system_error():
    message = 'test message'
    response = ResponseFailure.build_system_error(message)

    assert bool(response) is False
    assert response.type == ResponseFailure.SYSTEM_ERROR
    assert response.message == message
