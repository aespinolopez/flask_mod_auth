import pytest

from app.mod_auth.domain.models import User
from app.mod_auth.domain.domain_model import DomainModel
from app.mod_auth.repositories.users_repository import UsersRepository

user1 = User(
    username='user1',
    email='user1@gmail.com',
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


@pytest.fixture
def users():
    return [user1, user2, user3, user4, user5]


def _check_results(domain_models_list, data_list):
    assert len(domain_models_list) == len(data_list)
    assert all(isinstance(dm, DomainModel) for dm in domain_models_list)
    assert set(dm.email for dm in domain_models_list) == set(item['email'] for item in data_list)


