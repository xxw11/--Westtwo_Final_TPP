from flask import request, g
from flask_restful import reqparse, abort

from App.apis.movie_user.model_utils import get_movie_user
from App.ext import cache

parse = reqparse.RequestParser()
parse.add_argument("token",required=True,help="please input token")

def _verify():
    login_args = parse.parse_args()

    token = login_args.get("token")

    user_id = cache.get(token)

    user = get_movie_user(user_id)

    if not user:
        abort(401, msg="please input correct token")

    g.user = user
    g.auth = token

def login_required(fun):

    def wrapper(*args,**kwargs):

        _verify()

        return fun(*args,**kwargs)

    return wrapper

def require_permission(permission):
    def require_permission_wrapper(fun):
        def wrapper(*args, **kwargs):
            _verify()

            if not g.user.check_permission(permission):
                abort(403,msg='user can not access')

            return fun(*args,**kwargs)
        return wrapper
    return require_permission_wrapper