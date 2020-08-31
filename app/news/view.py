from flask import render_template, Blueprint, request, session, url_for, redirect
from werkzeug.utils import secure_filename

from app.model import News, Category
from app.news.form import NewsAddForm
from app.news.init import news

from app.news.utils import change_filename
from app.static.location import INDEX_IMAGE_DIR, VIDEO_DIR
from app.user.utils import user_login_req, admin_login_req


@news.route("/")
def index():
    news=News.query.filter_by(status=1)
    return render_template('index.html',news=news)

@news.route("/news/<int:id>/",methods=['GET', 'POST'])
def readnews(id):
    news=News.query.filter_by(id=id).first_or_404()
    video_exist =  news.video
    if (news.status != 1)&(session.get('is_admin')==0):
        return redirect(url_for('news.index'))
    return render_template('read_news.html',news=news,video_exist=video_exist)


@news.route("/addnews/", methods=['GET', 'POST'])
@user_login_req
def addnews():
    form=NewsAddForm()
    categorys = Category.query.all()

    if form.validate_on_submit():
        rform = request.form
        news=News()
        news.title=rform['title']
        news.digest=rform['digest']
        news.content=rform['content']
        news.source=rform['source']
        news.user_id=session.get('user_id')

        category=Category.query.filter_by(name=rform['category']).first()
        news.category_id=category.id
        news.category_name=category.name

        if form.index_image :
            index_image = secure_filename(form.index_image.data.filename)
            index_image = change_filename(index_image)
            form.index_image.data.save(INDEX_IMAGE_DIR + index_image)
            news.index_image_url=index_image

        if form.video :
            video = secure_filename(form.video.data.filename)
            video = change_filename(video)
            form.video.data.save(VIDEO_DIR + video)
            news.video = video

        if not news.save():
            return render_template('index.html')

        form = NewsAddForm()
        return render_template('add_news.html', form=form)

    return render_template('add_news.html',form=form,categorys=categorys)


@news.route("/filternews/<int:type>/",methods=['GET', 'POST'])
@admin_login_req
def filternews(type):
    news = None
    # 已经审核
    if type == 1:
        news = News.query.filter_by(status=1,is_delete=0)

    # 未审核
    elif type == 0:
        news = News.query.filter_by(status=0,is_delete=0)

    # 审核不通过
    elif type == 4:
        news = News.query.filter_by(status=4,is_delete=0)

    # 已删除
    elif type == 2 :
        news = News.query.filter_by(is_delete=1)
        return render_template('filter_news.html',news=news)
    # 所有
    elif type == 3 :
        news = News.query.all()
    return render_template('filter_news.html',news=news)

@news.route("/changestatus/<int:id><int:status>",methods=['GET', 'POST'])
@admin_login_req
def changestatus(id,status):
    news = News.query.filter_by(id=id).first_or_404()
    if status == 0:
        news.status=0
    elif status == 1:
        news.status=1
    elif status ==2:
        news.is_delete=1
    elif status ==4:
        news.status=4
    elif status ==5:
        news.is_delete=0
    news.save()
    return redirect(url_for('news.filternews',type=3))
