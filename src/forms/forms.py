from string import ascii_letters
from string import punctuation
from string import digits

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import EqualTo
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import StringField 
from wtforms import SubmitField


USERTAG_VALID_CHARS = set(*[ascii_letters + digits + punctuation])

class RegisterForm(FlaskForm):
    """Form used for user registering."""

    username = StringField("Username", validators=[Length(min=6, max=16)])
    usertag = StringField("Usertag", validators=[Length(min=8, max=14)])
    password = PasswordField("Password", validators=[Length(min=6)])

    repeat_password = PasswordField("Repeat password",
                                    validators=[EqualTo("password",
                                    message="Passwords must match.")])

    def validate_usertag(self, field):
        if not set(field.data) <= USERTAG_VALID_CHARS:
            raise ValueError("Invalid characters.")
        
        # Don't permit blank names
        elif set(field.data) == {' '}:
            raise ValueError("Invalid usertag.")
        
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    """Form used for logging in users"""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")

    submit = SubmitField("Login")


class QuoteInput(FlaskForm):
    """Form used for posting quotes on the application"""

    content = StringField("Quote content")
