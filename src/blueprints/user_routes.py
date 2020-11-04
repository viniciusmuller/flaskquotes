from flask import render_template
from flask import Blueprint
from flask import redirect
from flask import flash
from flask import abort
from flask_login import current_user
from flask_login import login_user

from utils.decorators import redirect_auth
from utils.decorators import templated
from utils.session import user_suggestions
from utils.session import validate_signup
from utils.session import validate_login
from utils.session import register_user
from utils.session import create_quote
from utils.session import find_user
from forms.forms import RegisterForm
from forms.forms import QuoteInput
from forms.forms import LoginForm


user_routes = Blueprint(name="user_routes", 
                        import_name=__name__,
                        template_folder="templates")


@user_routes.route('/', methods=["GET"])
@templated("social/index.html")
@redirect_auth()
def index():
    """Renders index page."""


@user_routes.route("/signup", methods=["GET", "POST"])
@templated("auth/sign_up.html")
@redirect_auth()
def sign_up():
    """Renders sign up page."""
    form = RegisterForm()

    if form.validate_on_submit():

        username: str = form.username.data
        usertag:  str = form.usertag.data
        password: str = form.password.data

        if validate_signup(usertag):
            user = register_user(username, usertag, password)
            login_user(user)
            return redirect(f"/user/{usertag}")

    return dict(form=form)


@user_routes.route("/login", methods=["GET", "POST"])
@templated("auth/login.html")
@redirect_auth()
def login():
    """Renders login page."""
    form = LoginForm()

    if form.validate_on_submit():

        username: str = form.username.data
        password: str = form.password.data
        remember: bool = form.remember_me.data

        if validate_login(username, password):
            user = find_user(username)
            login_user(user, remember=remember)
            return redirect(f"/user/{username}")
        else:
            flash("Invalid user credentials.")

    return dict(form=form)


@user_routes.route("/user/<string:usertag>", methods=["GET", "POST"])
@templated("social/profile.html")
def profile(usertag: str):
    """Main application page, this route renders the users profiles."""

    profile_owner = find_user(usertag)

    # User was not found
    if profile_owner is None:
        abort(404)

    quote_input = QuoteInput()

    if quote_input.validate_on_submit():
        create_quote(current_user, quote_input.content.data)

    suggestions = user_suggestions(user=current_user, 
                                   prof_owner=profile_owner,
                                   user_num=5)

    # Reversed quotes for chronologic view
    quotes = reversed(profile_owner.quotes)

    return dict(quote_input=quote_input, 
                rec_users=suggestions,
                user=profile_owner,
                quotes=quotes)
