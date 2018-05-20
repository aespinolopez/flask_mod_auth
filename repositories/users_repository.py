from app.mod_auth.domain.models import User
from datetime import datetime


class UsersRepository:

    _SUPPORTED_OPERATIONS = ['icontains']

    def __init__(self, entity):
        self.entity = entity

    def list(self, filters=None):
        self._check(filters)
        results = self.entity.objects(**filters, deleted_at=None)
        return [self._transform_to_domain(user) for user in results]

    def get_by_id(self, pk):
        user = self.entity.get(pk=pk)
        return self._transform_to_domain(user)

    def get_by_name(self, name):
        # todo may raise DoesNotExist or MultipleObjectsReturned
        user = self.entity.get(username=name)
        return self._transform_to_domain(user)

    def get_by_email(self, email):
        # todo may raise DoesNotExist or MultipleObjectsReturned
        user = self.entity.get(email=email)
        return self._transform_to_domain(user)

    def create_user(self, user):
        new_user = self.entity(
            username=user.username,
            email=user.email,
            password=user.password
        )
        self.entity.save()
        return self._transform_to_domain(new_user)

    def update_user(self, user):
        pass

    def delete_user(self, user):
        user_to_delete = self.entity.get(email=user.email)
        user_to_delete.deleted_at = datetime.utcnow()
        user_to_delete.save()
        return self._transform_to_domain(user_to_delete)

    def _check(self, filters):
        for filter_ in filters:
            if '__' in filter_:
                property_, operator = filter_.split('__')
                if operator not in self._SUPPORTED_OPERATIONS:
                    raise ValueError('Unsupported operation {}'.format(operator))

    def _transform_to_domain(self, user):
        return User(
            username=user.username,
            email=user.email,
            password=user.password
        )
