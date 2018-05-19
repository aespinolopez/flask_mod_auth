import json

from app.mod_auth.domain.models import User


class UserJsonSerializer(json.JSONEncoder):

    def default(self, user: User):
        try:
            to_serialize = {
                'username': user.username,
                'email': user.email,
                'password': user.password
            }
        except AttributeError:
            return super().default(user)
        else:
            return to_serialize
