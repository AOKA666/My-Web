from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms import ValidationError
from app.models import User
from flask_ckeditor import CKEditorField


class EditForm(FlaskForm):
    title = StringField('Please enter article title', validators=[DataRequired()])
    body = CKEditorField('Please write some articles', validators=[DataRequired()])
    submit = SubmitField('Submit')

