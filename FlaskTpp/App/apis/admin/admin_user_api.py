import uuid

from flask_restful import Resource, reqparse, abort, fields, marshal

from App.apis.admin.admin_model_utils import get_admin_user
from App.apis.api_constant import HTTP_CREATE_OK, USER_ACTION_REGISTER, USER_ACTION_LOGIN, HTTP_OK

from App.ext import cache
from App.models.admin.admin_user_model import AdminUser
from App.settings import ADMINS

parse_base = reqparse.RequestParser()
parse_base.add_argument("action", type=str, required=True, help="please input action")
parse_base.add_argument("password", type=str, required=True, help="please input password")
parse_base.add_argument("username", type=str, required=True, help="please input username")



admin_user_fields = {
    "username":fields.String,
    "password":fields.String(attribute="_password"),
}

single_admin_user_fields={
    "status":fields.Integer,
    "msg":fields.String,
    "data":fields.Nested(admin_user_fields)
}

class AdminUsersResource(Resource):

    def post(self):

        args = parse_base.parse_args()

        password = args.get("password")
        action = args.get("action").lower()
        username = args.get("username")

        if action == USER_ACTION_REGISTER:
            admin_user = AdminUser()
            admin_user.username = username
            admin_user.password = password

            if username in ADMINS:
                admin_user.is_super=1

            if not admin_user.save():
                abort(400,msg = "create fail")

            data = {
                "status":HTTP_CREATE_OK,
                "msg":"user created",
                "data":admin_user
            }
            return marshal(data, single_admin_user_fields)

        elif action == USER_ACTION_LOGIN:
            user = get_admin_user(username)
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