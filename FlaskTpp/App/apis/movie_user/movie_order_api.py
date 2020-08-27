from flask import g
from flask_restful import Resource, reqparse, abort

from App.apis.movie_user.model_utils import get_movie_user
from App.apis.movie_user.utils import login_required, require_permission
from App.ext import cache
from App.models.movie_user.movie_user_model import VIP_USER, COMMON_USER


class MovieOrdersResource(Resource):

    @login_required
    def post(self):

        user = g.user

        return {"msg":"post order ok"}

class MovieOrderResource(Resource):

    @require_permission(VIP_USER)
    def put(self,order_id):

        user =g.user

        if not user.check_permission(VIP_USER):
            abort(403,msg='user can not access')

        return {"msg":"change success"}