import pytest
from unittest import mock

from app.mod_auth.domain.models import User
from app.mod_auth.use_cases.list_users_use_case import ListUsersUseCase
from app.mod_auth.use_cases.requests_objects import ListUsersRequestObject
from app.mod_auth.use_cases.response_objects import ResponseFailure


@pytest.fixture()
def domain_users():
    user1 = User(
        username='user1',
        email='user12@gmail.com',
        password='1234'
    )
    user2 = User(
        username='user2',
        email='user2@gmail.com',
        password='1234'
    )
    user3 = User(
        username='user3',
        email='user3@gmail.com',
        password='1234'
    )
    user4 = User(
        username='user4',
        email='user4@gmail.com',
        password='1234'
    )
    user5 = User(
        username='user5',
        email='user5@gmail.com',
        password='1234'
    )

    return [user1, user2, user3, user4, user5]


def test_list_users_without_params(domain_users):
    repo = mock.Mock()
    repo.list.return_value = domain_users

    list_users_use_case = ListUsersUseCase(repo)
    request_object = ListUsersRequestObject.from_dict({})

    response_object = list_users_use_case.execute(request_object)

    assert bool(response_object) is True
    repo.list.assert_called_with(filters=None)

    assert response_object.value == domain_users


def test_list_users_with_filters(domain_users):
    repo = mock.Mock()
    repo.list.return_value = domain_users

    list_users_use_case = ListUsersUseCase(repo)
    query_filters = {'a': 5}
    request_object = ListUsersRequestObject.from_dict({'filters': query_filters})

    response_object = list_users_use_case.execute(request_object)

    assert bool(response_object) is True
    repo.list.assert_called_with(filters=query_filters)
    assert response_object.value == domain_users


def test_list_users_handles_generic_error():
    repo = mock.Mock()
    repo.list.side_effect = Exception('Just an error message')

    list_users_use_case = ListUsersUseCase(repo)
    request_object = ListUsersRequestObject.from_dict({})

    response_object = list_users_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'type': ResponseFailure.SYSTEM_ERROR,
        'message': 'Exception: Just an error message'
    }


def test_list_users_handles_bad_request():
    repo = mock.Mock()

    list_users_use_case = ListUsersUseCase(repo)
    request_object = ListUsersRequestObject.from_dict({'filters': 5})

    response_object = list_users_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'type': ResponseFailure.PARAMETERS_ERROR,
        'message': 'filters: Is not iterable'
    }
