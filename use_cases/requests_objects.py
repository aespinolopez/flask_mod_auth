import collections


class InvalidRequestObject:

    def __init__(self):
        self.errors = []

    def add_error(self, parameter, message):
        self.errors.append({'parameter': parameter, 'message': message})

    def has_errors(self):
        return len(self.errors) > 0

    def __bool__(self):
        return False


class ValidRequestObject:

    @classmethod
    def from_dict(cls, data):
        raise NotImplementedError

    def __bool__(self):
        return True


class ListUsersRequestObject(ValidRequestObject):

    def __init__(self, filters=None):
        # todo maybe control if filters is iterable here too
        self.filters = filters

    @classmethod
    def from_dict(cls, data):
        invalid_req = InvalidRequestObject()

        if 'filters' in data and not isinstance(data['filters'], collections.Mapping):
            invalid_req.add_error('filters', 'Is not iterable')

        if invalid_req.has_errors():
            return invalid_req

        return ListUsersRequestObject(filters=data.get('filters', None))

    def __bool__(self):
        return True
