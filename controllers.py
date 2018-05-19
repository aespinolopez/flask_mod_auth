from flask import Blueprint, jsonify, request, abort
from flask.views import MethodView
from app.utils.flask_utils import register_api
from .exceptions import ApiQueryError, ValidationError
from .models import UsersModel, User, query_to_json, ph
from .validations import is_valid_email
from argon2.exceptions import VerificationError
from mongoengine.errors import NotUniqueError


mod_auth = Blueprint('auth', __name__, url_prefix='/')

_SORT_ACTION = 'sort'
_SEARCH_ACTION = 'search'
_FILTER_ACTION = 'filter'
_PAGINATE_ACTION = 'page'


# todo test pagination
# todo implement error handlers and control possible filter_users exception when key not found
# todo reset password and forgot password system
# todo internationzalization
# todo comment code


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
            if _PAGINATE_ACTION in arguments:
                query = UsersModel.paginate(query, arguments[_PAGINATE_ACTION])
            data = query_to_json(query)
            return jsonify(data)

    def post(self):
        json = request.get_json()
        try:
            user = User.from_json(json)
            model = UsersModel.persist(user)
        except NotUniqueError:
            abort(409)
        except ValidationError as err:
            abort(400, err.message)

        else:
            return jsonify(model.to_json()), 201

    def put(self, user_id):
        json = request.get_json()
        user = UsersModel.get_user(user_id)
        try:
            user.username = json['username']
            user.email = json['email']
        except ValidationError as err:
            abort(400, err.message)

        UsersModel.persist(user)
        return jsonify(user.to_json())

    def delete(self, user_id):
        model = UsersModel.get_model(user_id)
        model.remove()
        return jsonify(User.from_model(model).to_json())

    @staticmethod
    def __process_get_arguments():
        arguments = {}
        for key, value in request.args.items():
            if key.lower() == _SORT_ACTION:
                arguments[_SORT_ACTION] = value
            elif key.lower() == _SEARCH_ACTION:
                arguments[_SEARCH_ACTION] = value
            elif key.lower == _PAGINATE_ACTION:
                arguments[_PAGINATE_ACTION] = value
            else:
                if _FILTER_ACTION not in arguments:
                    arguments[_FILTER_ACTION] = {}
                arguments[_FILTER_ACTION][key] = value

        if _FILTER_ACTION in arguments and _SEARCH_ACTION in arguments:
            raise ApiQueryError('cannot filter and search results in the same request')

        return arguments


@mod_auth.route('/authenticate', methods=['POST'])
def authenticate():
    json = request.get_json()
    if is_valid_email(json['identifier']):
        user = UsersModel.filter_users(email=json['identifier']).first()
    else:
        user = UsersModel.filter_users(username=json['identifier']).first()
    if not user:
        abort(404, 'user not found')
    try:
        ph.verify(user.password, json['password'])
    except VerificationError:
        abort(401, 'passwords doesn\'t match')
    return '', 204


register_api(mod_auth, UsersApi, 'users_api', '/users/', 'user_id', 'string')
