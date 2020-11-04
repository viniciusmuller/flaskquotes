import functools

from flask_login import current_user
from flask import render_template
from flask import redirect

from exts import db


def redirect_auth(endpoint=None):
    """Redirects the user to the given endpoint if authenticated"""
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):

            # Redirect to user profile if any other route is provided.
            if current_user.is_authenticated and endpoint is None:
                return redirect(f"/user/{current_user.usertag}")

            else:
                return f(*args, **kwargs)

        return wrapper
    return decorator


def templated(template: str):
    """Render a template"""
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):

            # The function must return a dictionary that
            # will be used to populate the Jinja2 template.
            ctx = f(*args, **kwargs)

            if ctx is None:
                ctx = {}

            # Returns ctx object if the route doesn't return a dict
            elif not isinstance(ctx, dict):
                return ctx

            return render_template(template, **ctx)
        return wrapper
    return decorator


def commit(add=True):
    """Commits the database after running the function.

    Parameter
    ---------
    add : `bool`
        If True, adds the function return
        to the database before commiting.
    """

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):

            result = f(*args, **kwargs)

            if add:
                db.session.add(result)

            db.session.commit()

            return result
        return wrapper
    return decorator


def login_required(f):
    """If the current user is not logged in,
    he gets redirected to /login.
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):

        if not current_user.is_authenticated:
            return redirect("/login")
        
        result = f(*args, **kwargs)

        return result
    return wrapper
