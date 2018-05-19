from app.mod_auth.domain.models import User

USERNAME_VALUE = 'EspinoKiller'
EMAIL_VALUE = 'espinokiller@gmail.com'
PASSWORD_VALUE = '1234'


def test_user_model_init():

    user = User(
        username=USERNAME_VALUE,
        email=EMAIL_VALUE,
        password=PASSWORD_VALUE
    )
    assert user.username == USERNAME_VALUE
    assert user.email == EMAIL_VALUE
    assert user.password == PASSWORD_VALUE


def test_user_model_from_dict():
    user = User.from_dict(
        {
            'username': USERNAME_VALUE,
            'email': EMAIL_VALUE,
            'password': PASSWORD_VALUE
        }
    )
    assert user.username == USERNAME_VALUE
    assert user.email == EMAIL_VALUE
    assert user.password == PASSWORD_VALUE
