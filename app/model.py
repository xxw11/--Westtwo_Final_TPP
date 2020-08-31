from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from app.ext import db

tb_user_collection = db.Table(
    "info_user_collection",
    db.Column("user_id", db.Integer, db.ForeignKey("info_user.id"), primary_key=True),  # 新闻编号
    db.Column("news_id", db.Integer, db.ForeignKey("info_news.id"), primary_key=True),  # 分类编号
    db.Column("create_time", db.DateTime, default=datetime.now)  # 收藏创建时间
)


class BaseModel(db.Model):
    __abstract__ = True
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间

    def save(self):
        try:

            db.session.add(self)

            db.session.commit()

            return True
        except Exception as e:
            print(e)

            return False

    def delete(self):
        try:
            db.session.delete(self)

            db.session.commit()

            return True
        except Exception as e:
            print(e)

            return False

class User(BaseModel):
    """用户"""
    __tablename__ = "info_user"
    email = db.Column(db.String(128), unique=True)
    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    nick_name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    # money = db.Column(db.Integer)
    avatar_url = db.Column(db.String(256))  # 用户头像路径
    last_login = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间
    is_admin = db.Column(db.Boolean, default=False)
    signature = db.Column(db.String(512))  # 用户签名
    # gender = db.Column(  # 订单的状态
    #     db.Enum(
    #         "MAN",  # 男
    #         "WOMAN"  # 女
    #     ),
    #     default="MAN")

    # 当前用户收藏的所有新闻
    collection_news = db.relationship("News", secondary=tb_user_collection, lazy="dynamic")  # 用户收藏的新闻
    # 用户所有的粉丝，添加了反向引用followed，代表用户都关注了哪些人
    # followers = db.relationship('User',
    #                             secondary=tb_user_follows,
    #                             primaryjoin=id == tb_user_follows.c.followed_id,
    #                             secondaryjoin=id == tb_user_follows.c.follower_id,
    #                             backref=db.backref('followed', lazy='dynamic'),
    #                             lazy='dynamic')


    # 当前用户所发布的新闻
    # news_list = db.relationship('News', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError("当前属性不可读")

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class News(BaseModel):
    """新闻"""
    __tablename__ = "info_news"

    id = db.Column(db.Integer, primary_key=True)  # 新闻编号
    title = db.Column(db.String(256), nullable=False)  # 新闻标题
    source = db.Column(db.String(64), nullable=False)  # 新闻来源
    digest = db.Column(db.String(512), nullable=False)  # 新闻摘要
    content = db.Column(db.Text, nullable=False)  # 新闻内容
    clicks = db.Column(db.Integer, default=0)  # 浏览量
    index_image_url = db.Column(db.String(256))  # 新闻列表图片路径
    video = db.Column(db.String(256)) #新闻视频路径
    category_id = db.Column(db.Integer, db.ForeignKey("info_category.id"))
    category_name = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey("info_user.id"))  # 当前新闻的作者id
    status = db.Column(db.Integer, default=0)  # 当前新闻状态 如果为0代表审核中，1代表审核过，4代表审核不通过,2删除
    reason = db.Column(db.String(256))  # 未通过原因，status = -1 的时候使用
    is_delete = db.Column(db.Integer,default=0)
    # 当前新闻的所有评论
    # comments = db.relationship("Comment", lazy="dynamic")

class Category(BaseModel):
    """新闻分类"""
    __tablename__ = "info_category"

    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    name = db.Column(db.String(64), nullable=False)  # 分类名
    news_list = db.relationship('News', backref='category', lazy='dynamic')