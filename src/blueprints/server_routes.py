from flask import Blueprint
from flask import redirect
from flask import jsonify
from flask import request
from flask import abort
from flask_login import current_user
from flask_login import logout_user

from utils.session import create_quote
from utils.session import find_user

 
server_routes = Blueprint(name="server_routes",
                          import_name=__name__,
                          template_folder="templates")


@server_routes.route("/delete/<int:quote_id>", methods=["DELETE"])
def remove_quote(quote_id: int):
    """Removes the given ID quote from the database.

    Notes
    -----
    - If the user is anonymous, he is redirected to /login;
    - If the user is not the owner of the quote, a 401 status is raised;
    - If the quote does not exist, a 404 status code is raised.
    """

    try:
        current_user.remove_quote(quote_id)
    except:
        abort(401)
    
    return jsonify(
        status="success"
    )


@server_routes.route("/post", methods=["POST"])
def post_quote():
    """Receives a POST request and validates it content.
    
    Notes
    -----
    If the quote posted by the user validate,
    adds it to the database.
    """

    if not current_user.is_authenticated:
        abort(401)

    content = request.form.get("content", '')

    if 0 < len(content) < 150:
        # Successful post
        quote = create_quote(current_user, content)

        return jsonify(
            content=content,
            timestamp=quote.fmt_time,
            success=True,
            id=quote.id
        )

    # Post failed validation
    return jsonify(
        success=False,
        reason="Quote length must be lesser than 150 characters."
    )


@server_routes.route("/follow/<string:usertag>")
def follow(usertag: str):
    """Follow the user given at endpoint and redirect to his profile.
    
    Notes
    -----
    - If the user does not exist, a 404 status code is raised.
    """
    user = find_user(usertag)

    if user is None:
        abort(404)

    if auth := current_user.is_authenticated:
        current_user.follow(user)

    # This is used on clientside in order to redirect an unauthenticated
    # user to the login page, any user changes into clientside javascript
    # will not affect serverside behaviour.
    return jsonify(
        authenticated=auth
    )

@server_routes.route("/unfollow/<string:usertag>")
def unfollow(usertag: str):
    """
    Follows the at the given endpoint
    
    Notes
    -----
    - If the user does not exist, a 404 status code is raised.
    """
    user = find_user(usertag)

    if user is None:
        abort(404)

    if auth := current_user.is_authenticated:
        current_user.unfollow(user)

    return jsonify(
        authenticated=auth
    )


@server_routes.route("/logout")
def logout():
    """Ends a flask_login user session."""

    if current_user.is_authenticated:
        logout_user()

    return redirect('/')
