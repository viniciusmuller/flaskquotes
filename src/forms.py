from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    """Form used for user registering"""

    username = StringField('username', validators=[Length(min=8, max=16)])
    usertag = StringField('usertag', validators=[Length(min=8, max=14)])
    password = PasswordField('password', validators=[Length(min=6)])
    repeat_password = PasswordField('repeat password',
                                    validators=[EqualTo('password',
                                    message='Passwords must match')])

    # Custom validators
    def validate_username(form, field):
        if not field.data.isalnum():
            raise ValueError('Name must be alphanumeric.')

    def validate_usertag(form, field):
        if not field.data.isalnum():
            raise ValueError('Name must be alphanumeric.')

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """Form used for logging in users"""

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('Login')


class QuoteInput(FlaskForm):
    """Form used for posting quotes on the application"""

    quote_content = StringField('quotecontent', validators=[DataRequired(), Length(max=150)])