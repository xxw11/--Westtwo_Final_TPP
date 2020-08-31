import uuid
from datetime import date, datetime

from flask import render_template, Blueprint, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from app.model import User
from app.news.utils import change_filename
from app.settings import ADMINS
from app.static.location import AVATAR_URL_DIR
from app.user.form import RegistForm, LoginForm, ChangeInfoForm
from app.user.init import user

# blue = Blueprint('blue', __name__)

@user.route("/login",methods=['GET', 'POST'])
def login():
    form=LoginForm()
    print('123')
    if request.method=='POST':
        data = form.data
        user = User.query.filter_by(email=data['email']).first()

        if user is None:
            flash('密码或账号错误', 'err')
            return redirect(url_for('user.login'))
        if not user.check_password(data['pwd']):
            print(user.check_password(data['pwd']))
            flash('密码或账号错误', 'err')
            return redirect(url_for('user.login'))

        session['user'] = user.nick_name
        session['user_id'] = user.id
        session['icon']=user.avatar_url
        session['is_admin']=user.is_admin
        user.last_login = datetime.now
        user.save()
        return redirect(url_for('news.index'))
    return render_template('login.html',form=form)

@user.route("/register",methods=['GET', 'POST'])
def register():
    form=RegistForm()
    if form.validate_on_submit():
        data = form.data
        email_count = User.query.filter_by(email=data['email']).count()
        if email_count == 1:
            flash("邮箱已经存在了", 'err')
            return redirect(url_for('user.register'))
        user = User(
            nick_name=data['nick_name'],
            email=data['email'],
            password=data['pwd'],
        )
        if user.nick_name in ADMINS:
            user.is_admin=1
        user.avatar_url="icon.jpg"
        user.save()
        flash('操作成功', 'ok')
        return redirect(url_for('user.login'))
    return render_template('register.html',form=form)

@user.route("/logout")
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    session.pop('icon', None)
    session.pop('is_admin',None)
    return redirect(url_for('user.login'))

@user.route("/info/<int:id>",methods=['GET', 'POST'])
def info(id):
    user = User.query.filter_by(id=id).first_or_404()
    form = ChangeInfoForm()
    if form.validate_on_submit()&(session.get('user_id')==user.id):
        data = form.data
        user = User.query.filter_by(id=session.get('user_id')).first_or_404()

        if form.avatar_url.data.filename:
            avatar_url = secure_filename(form.avatar_url.data.filename)
            avatar_url = change_filename(avatar_url)
            form.avatar_url.data.save(AVATAR_URL_DIR + avatar_url)
            user.avatar_url = avatar_url

        user.nick_name=data['nick_name'] or user.nick_name
        user.signature=data['signature'] or user.signature
        user.save()
        return redirect(url_for('user.info',id=user.id))
    return render_template('userinfo.html',user=user,form=form)

