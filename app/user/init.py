from flask import Blueprint, render_template


def init_user(app):
    @app.errorhandler(404)
    def hello(e):
        return render_template('404.html')
    app.register_blueprint(user)

user = Blueprint('user', __name__,url_prefix="/user")
import app.user.view