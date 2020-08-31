from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, RadioField, \
    BooleanField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length, Email, Regexp
class RegistForm(FlaskForm):
    nick_name = StringField(
        label="账号",
        validators=[
            # DataRequired("请输入账号")
        ],
        description='账号',
        render_kw={

            "class": "form-control round",
            "placeholder": "请输入你的昵称",

        },

    )
    email = StringField(
        label="邮箱",
        validators=[
            # DataRequired("请输入邮箱"),
            Email("邮箱格式不正确"),
        ],
        description='邮箱',
        render_kw={
            "class": "form-control round",
            "placeholder": "请输入你的邮箱",

        }
    )

    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        description='密码',
        render_kw={
            "class": "form-control round",
            "placeholder": "请输入密码",
            "required": "required"
        }
    )
    usericon = FileField(
        label="头像",
        render_kw={
            "required": "required"
        }
    )
    repwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请确认密码"),
            EqualTo('pwd', message='两次密码不一致')
        ],
        description='密码',
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码",
            "required": "required"
        }
    )
    submit = SubmitField(
        '注册',
        render_kw={
            "class": "btn btn-primary btn-round btn-block",
        }
    )
class LoginForm(FlaskForm):

    email = StringField(
        label="邮箱",

        description='邮箱',
        render_kw={
            "class": "form-control round",
            "placeholder": "请输入你的邮箱",

        }
    )
    pwd = PasswordField(
        label="密码",
        description='密码',
        render_kw={
            "class": "form-control round",
            "placeholder": "请输入密码",
            "required": "required"
        }
    )
    checkbox = BooleanField(
        label="记住我",
        render_kw={
        }
    )
    submit = SubmitField(
        '确认',
        render_kw={
            "class": "btn btn-lg btn-info btn-block",
        }
    )
class ChangeInfoForm(FlaskForm):
    nick_name = StringField(
        label="修改新的昵称",
        description='昵称',
        render_kw={

            "class": "form-control",
            "placeholder": "修改新的昵称",

        },

    )
    signature = StringField(
        label="修改新的签名",
        description='签名',
        render_kw={

            "class": "form-control",
            "placeholder": "修改新的签名",

        },

    )
    avatar_url = FileField('用户头像上传',
    validators=[FileAllowed(['png', 'JPEG', 'jpg'],
    '只能上传图片！')]
    )
    submit = SubmitField(
        '更新',
        render_kw={
            "class": "btn btn-round btn-primary",
        }
    )