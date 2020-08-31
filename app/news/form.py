from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length, Email, Regexp

class NewsAddForm(FlaskForm):
    title = StringField(
        label="新闻标题",
        validators=[
            DataRequired("请输入新闻标题")
        ],
        description='新闻标题',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新闻标题",
            "required": "required"
        },

    )
    source = StringField(
        label="新闻来源",
        validators=[
            DataRequired("请输入新闻来源")
        ],
        description='新闻来源',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新闻来源",
            "required": "required"
        },

    )
    digest = StringField(
        label="新闻摘要",
        validators=[
            DataRequired("请输入新闻摘要")
        ],
        description='新闻摘要',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新闻摘要",
            "required": "required"
        },

    )
    content = TextAreaField(
        label="新闻内容",
        validators=[
            DataRequired("请输入新闻内容")
        ],
        description='新闻内容',
        render_kw={
            'class':"form-control",
            "rows":5,
            "cols":30,
            "required": "required",
        },
    )
    index_image = FileField('图片上传',
    validators=[FileAllowed(['png', 'JPEG', 'jpg'],
    '只能上传图片！'),
    FileRequired('文件未选择！')])

    video = FileField(
        '视频上传',
        validators=[FileAllowed(['mp4']
        , '只能上传视频！')])

    submit = SubmitField(
        '确认',
        render_kw={
            "class": "btn btn-primary",
        }
    )


