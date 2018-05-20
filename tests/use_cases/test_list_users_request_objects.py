from app.mod_auth.use_cases.requests_objects import ListUsersRequestObject


def test_build_list_users_request_object_without_params():
    request = ListUsersRequestObject()

    assert request.filters is None
    assert bool(request) is True


def test_build_list_users_request_object_from_empty_dict():
    request = ListUsersRequestObject.from_dict({})

    assert request.filters is None
    assert bool(request) is True


def test_build_list_users_request_object_with_empty_filters():
    request = ListUsersRequestObject(filters={})

    assert request.filters == {}
    assert bool(request) is True


def test_build_list_users_request_object_from_dict_with_empty_filters():
    request = ListUsersRequestObject.from_dict({'filters': {}})

    assert request.filters == {}
    assert bool(request) is True


def test_build_list_users_request_object_with_filters():
    filters = {'a': 1, 'b': 2}
    request = ListUsersRequestObject(filters=filters)

    assert request.filters == filters
    assert bool(request) is True


def test_build_list_users_request_object_from_dict_with_filters():
    filters = {'a': 1, 'b': 2}
    request = ListUsersRequestObject.from_dict({'filters': filters})

    assert request.filters == filters
    assert bool(request) is True


def test_build_list_users_request_object_from_dict_with_invalid_filters():
    request = ListUsersRequestObject.from_dict({'filters': 5})

    assert request.has_errors()
    assert request.errors[0]['parameter'] == 'filters'
    assert bool(request) is False
