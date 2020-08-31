from flask import Blueprint, render_template


def init_news(app):
    @app.errorhandler(404)
    def hello(e):
        return render_template('404.html')
    app.register_blueprint(news)

news = Blueprint('news', __name__,)
import app.model
import app.news.view
