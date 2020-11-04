from flask import render_template
from flask import Blueprint


error_handling = Blueprint(name="error_handling",
                          import_name=__name__,
                          static_folder="templates")


@error_handling.app_errorhandler(404)
def not_found(err):
    return render_template("errors/404.html"), 404


@error_handling.app_errorhandler(401)
def not_found(err):
    return render_template("errors/401.html"), 401
