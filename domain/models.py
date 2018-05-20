from app.mod_auth.domain.domain_model import DomainModel


class User(DomainModel):

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @classmethod
    def from_dict(cls, data):
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )

        return user
