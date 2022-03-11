from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms import ValidationError
from app.models import User
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    # email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('保持登录状态')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '重复密码', validators=[DataRequired(), EqualTo('密码')])
    submit = SubmitField('注册')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名已存在')
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('邮箱地址已存在')


class CommentForm(FlaskForm):
    body = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('发表评论')


class ChangeAvatarForm(FlaskForm):
    avatar = FileField('')
    submit = SubmitField('提交')
    

class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')
    
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('用户名已存在')
                

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('请输入邮箱', validators=[DataRequired(), Email()])
    submit = SubmitField('发送')
    

class ResetPasswordForm(FlaskForm):
    password = PasswordField('请输入密码', validators=[DataRequired()])
    password2 = PasswordField('请再次输入密码', validators=[DataRequired(), EqualTo('请输入密码')])
    submit = SubmitField('重置密码')