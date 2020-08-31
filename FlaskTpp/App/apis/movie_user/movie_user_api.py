import uuid

from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.api_constant import HTTP_CREATE_OK, USER_ACTION_REGISTER, USER_ACTION_LOGIN, HTTP_OK
from App.apis.movie_user.model_utils import get_movie_user
from App.ext import cache
from App.models.movie_user import MovieUser

parse_base = reqparse.RequestParser()
parse_base.add_argument("action", type=str, required=True, help="please input action")
parse_base.add_argument("password", type=str, required=True, help="please input password")

parse_register = parse_base.copy()
parse_register.add_argument("username", type=str, required=True, help="please input username")
parse_register.add_argument("phone", type=str, required=True, help="please input phone")

parse_login = parse_base.copy()
parse_login.add_argument("username", type=str, help="please input username")
parse_login.add_argument("phone", type=str,  help="please input phone")


movie_user_fields = {
    "username":fields.String,
    "password":fields.String(attribute="_password"),
    "phone":fields.String,
}

single_movie_user_fields={
    "status":fields.Integer,
    "msg":fields.String,
    "data":fields.Nested(movie_user_fields)
}

class MovieUsersResource(Resource):

    def post(self):

        args = parse_base.parse_args()

        password = args.get("password")
        action = args.get("action").lower()

        if action == USER_ACTION_REGISTER:

            args_register = parse_register.parse_args()
            phone = args_register.get("phone")
            username = args_register.get("username")

            movie_user = MovieUser()
            movie_user.username = username
            movie_user.password = password
            movie_user.phone = phone

            if not movie_user.save():
                abort(400,msg = "create fail")

            data = {
                "status":HTTP_CREATE_OK,
                "msg":"user created",
                "data":movie_user
            }
            return marshal(data,single_movie_user_fields)

        elif action == USER_ACTION_LOGIN:
            args_login = parse_login.parse_args()
            phone = args_login.get("phone")
            username = args_login.get("username")
            print(username)
            user = get_movie_user(username) or get_movie_user(phone)
            print(user)
            if not user:
                abort(400,msg="user don't exist")

            if not user.check_password(password):
                abort(401,msg="wrong password")

            if user.is_delete:
                abort(401,msg="user don't exist")
            token = uuid.uuid4().hex

            cache.set(token,user.id,timeout=60*60*24*7)

            data = {
                "msg":"login success",
                "status":HTTP_OK,
                "token":token,
            }
            return data

        else:
            abort(400,msg="please check your parameters")