from functools import wraps

from flask import session, flash, redirect, url_for, request

from app.model import User


def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            flash('请先登录', 'err')
            return redirect(url_for('user.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function

def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user=User.query.get(session['user_id'])
        if user is None:
            return redirect(url_for('news.index', next=request.url))
        return f(*args, **kwargs)

    return decorated_function
