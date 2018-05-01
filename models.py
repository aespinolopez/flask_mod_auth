from app import db
from datetime import datetime
from argon2 import PasswordHasher
from .exceptions import ValidationError
from .validations import (
    is_valid_username,
    is_valid_email,
    check_length,
    has_uppercase,
    has_digit,
    has_lowercase,
    has_special_char
)

ph = PasswordHasher()


class UsersModel(db.Document):
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.utcnow())
    updated_at = db.DateTimeField()
    deleted_at = db.DateTimeField()

    @db.queryset_manager
    def list_users(doc_cls, queryset):
        return queryset.filter(deleted_at=None)

    @staticmethod
    def get_user(user_id):
        model = UsersModel.objects.get(pk=user_id)
        return User.from_model(model)

    @staticmethod
    def get_model(user_id):
        return UsersModel.objects.get(pk=user_id)

    @staticmethod
    def filter_users(**kwargs):
        query = UsersModel.objects(**kwargs, deleted_at=None)
        return query

    @staticmethod
    def search_users(username):
        query = UsersModel.objects(username__icontains=username, deleted_at=None)
        return query

    @staticmethod
    def sorted_by(field, query):
        return query.order_by(field)

    @staticmethod
    def persist(user):
        user_model = UsersModel.from_user(user)
        user_model.save()
        return user_model

    @staticmethod
    def from_user(user):
        if user.user_id == 0:
            user_model = UsersModel(
                username=user.username,
                email=user.email,
                password=user.password
            )
        else:
            user_model = UsersModel.get_model(user.user_id)
            user_model.username = user.username
            user_model.email = user.email
            user_model.updated_at = datetime.utcnow()

        return user_model

    def remove(self):
        self.deleted_at = datetime.utcnow()
        self.save()

    def to_json(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class User:

    @staticmethod
    def from_json(json):
        return User(json['username'], json['email'], json['password'])

    @staticmethod
    def from_model(model):
        user = User(model.username, model.email, user_id=model.id)
        user._password = model.password
        return user

    def __init__(self, username, email, password=None, user_id=0):
        self.user_id = user_id
        self.username = username
        self.email = email
        if password:
            self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        errors = _validate_password(password)
        if not errors:
            self._password = ph.hash(password)
        else:
            raise ValidationError('password', errors)

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        errors = _validate_username(username)
        if not errors:
            self._username = username
        else:
            raise ValidationError('username', errors)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if is_valid_email(email):
            self._email = email
        else:
            raise ValidationError('email', ['{} is not a valid'.format(email)])

    def to_json(self):
        return {
            'id': str(self.user_id),
            'username': self.username,
            'email': self.email
        }


def query_to_json(query):
    users = []
    for user_model in query:
        user = User.from_model(user_model)
        users.append(user.to_json())

    return users


def _validate_username(username):
    length_range = (3, 20)
    errors = []
    if not is_valid_username(username):
        errors.append('should contain only letters, digits, underscore and hyphens')
    if not check_length(username, length_range[0], length_range[1]):
        errors.append('should has at least {} characters and a maximum of {}'.format(length_range[0], length_range[1]))

    return errors


def _validate_password(password):
    length_range = (6, 20)
    errors = []
    if not has_digit(password):
        errors.append('should contain at least one digit')
    if not has_uppercase(password):
        errors.append('should contain at least an uppercase letter')
    if not has_lowercase(password):
        errors.append('should contain at least a lowercase letter')
    if not has_special_char(password):
        errors.append('should contain at least a special character')
    if not check_length(password, length_range[0], length_range[1]):
        errors.append('length should be between {} and {}'.format(length_range[0], length_range[1]))

    return errors

# todo think about a generic validate(field, functions) function


