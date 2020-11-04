from flask import Blueprint
from flask import redirect
from flask import abort
from flask_login import current_user
from flask_login import logout_user

from utils.decorators import login_required
from utils.session import find_user

 
server_routes = Blueprint(name="server_routes",
                          import_name=__name__,
                          template_folder="templates")


@server_routes.route("/delete/<int:quote_id>")
@login_required
def remove_quote(quote_id: int):
    """Removes the given ID quote from the database.
    
    Notes
    -----
    - If the user is anonymous, he is redirected to /login;
    - If the user is not the owner of the quote, a 401 status is raised;
    - If the quote does not exist, a 404 status code is raised.
    """

    quote = current_user._quotes.filter_by(id=quote_id).first()

    if quote not in current_user._quotes:
        abort(401)
    else:
        current_user.remove_quote(quote)

    return redirect(f"/user/{current_user.usertag}")

    # If the quote doesn't exist
    return abort(404)


@server_routes.route("/follow/<string:usertag>")
@login_required
def follow(usertag: str):
    """Follow the user given at endpoint and redirect to his profile.
    
    Notes
    -----
    - If the user is anonymous, he is redirected to /login;
    - If the user does not exist, a 404 status code is raised.
    """
    user = find_user(usertag)

    if user is None:
        abort(404)

    current_user.follow(user)

    return redirect(f"/user/{usertag}")


@server_routes.route("/unfollow/<string:usertag>")
@login_required
def unfollow(usertag: str):

    user = find_user(usertag)

    if user is None:
        abort(404)

    current_user.unfollow(user)

    return redirect(f"/user/{usertag}")


@server_routes.route("/logout")
@login_required
def logout():
    """Ends a flask_login user session."""
    logout_user()
    return redirect('/')
