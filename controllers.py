from flask import Blueprint, jsonify, request
from flask.views import MethodView
from app.utils.flask_utils import register_api
from .exceptions import ApiQueryError
from .models import UsersModel, User, query_to_json


mod_auth = Blueprint('auth', __name__, url_prefix='/')

_SORT_ACTION = 'sort'
_SEARCH_ACTION = 'search'
_FILTER_ACTION = 'filter'
_PAGINATE_ACTION = 'page'


# todo set pagination
# todo test api


class UsersApi(MethodView):

    def get(self, user_id):
        self.__process_get_arguments()
        if user_id:
            user = UsersModel.get_user(user_id)
            return jsonify(user.to_json())
        else:
            arguments = UsersApi.__process_get_arguments()
            if _SEARCH_ACTION in arguments:
                query = UsersModel.search_users(arguments[_SEARCH_ACTION])
            elif _FILTER_ACTION in arguments:
                query = UsersModel.filter_users(**arguments[_FILTER_ACTION])
            else:
                query = UsersModel.list_users()
            if _SORT_ACTION in arguments:
                query = UsersModel.sorted_by(arguments[_SORT_ACTION], query)
            data = query_to_json(query)
            return jsonify(data)

    def post(self):
        json = request.get_json()
        # todo validate content
        user = User.from_json(json)
        model = UsersModel.persist(user)
        return jsonify(model.to_json())

    def put(self, user_id):
        json = request.get_json()
        user = UsersModel.get_user(user_id)
        user.username = json['username']
        user.email = json['email']
        user.password = json['password']
        UsersModel.from_user(user).persist()
        return user.to_json()

    def delete(self, user_id):
        model = UsersModel.get_model(user_id).delete()
        model.remove()
        return User.from_model(model).to_json()

    @staticmethod
    def __process_get_arguments():
        arguments = {}
        for key, value in request.args.items():
            if key.lower() == _SORT_ACTION:
                arguments[_SORT_ACTION] = value
            elif key.lower() == _SEARCH_ACTION:
                arguments[_SEARCH_ACTION] = value
            elif key.lower == _PAGINATE_ACTION:
                pass
            else:
                if _FILTER_ACTION not in arguments:
                    arguments[_FILTER_ACTION] = {}
                arguments[_FILTER_ACTION][key] = value

        if _FILTER_ACTION in arguments and _SEARCH_ACTION in arguments:
            raise ApiQueryError('cannot filter and search results in the same request')

        return arguments


register_api(mod_auth, UsersApi, 'users_api', '/users/', 'user_id', 'string')
