from flask import Flask

from app.ext import init_ext
from app.news.init import init_news
from app.settings import envs
# from app.news.init import init_news
from app.user.init import init_user


def create_app(env):
    app = Flask(__name__)

    app.config.from_object(envs.get(env))

    init_ext(app)

    init_user(app=app)

    init_news(app=app)
    return app