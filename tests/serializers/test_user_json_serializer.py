import json

from app.mod_auth.domain.models import User
from app.mod_auth.serializers.user_json_serializer import UserJsonSerializer

USERNAME_VALUE = 'EspinoKiller'
EMAIL_VALUE = 'espinokiller@gmail.com'
PASSWORD_VALUE = '1234'


def test_serialize_domain_user():
    user = User(
        username=USERNAME_VALUE,
        email=EMAIL_VALUE,
        password=PASSWORD_VALUE
    )

    expected_json = """
    {{
        "username": "{username}",
        "email": "{email}",
        "password": "{password}"
    }}
    """.format(username=USERNAME_VALUE, email=EMAIL_VALUE, password=PASSWORD_VALUE)

    assert json.loads(json.dumps(user, cls=UserJsonSerializer)) == json.loads(expected_json)
