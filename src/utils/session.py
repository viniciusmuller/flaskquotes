from typing import Optional
from random import sample, randint

from utils.decorators import commit
from database.tables import Quote
from database.tables import User


def find_user(usersearch: str) -> Optional[User]:
    """Search for a user either by name or tag and returns it

    Parameters
    ----------
    usersearch : `str`
        A username or usertag

    Return
    ------
    user : `User`
        Requested user instance

    Notes
    -----
    If the user is not found, returns None
    """

    user = User.query.filter_by(usertag=usersearch).first() \
           or User.query.filter_by(username=usersearch).first()

    return user


def validate_signup(usertag: str) -> bool:
    """Checks if the usertag already exists before signup

    Parameter
    ---------
    usertag : `str`
        Usertag

    Return
    ------
    result : `bool`
        User already exists in the database
    """

    user = User.query.filter_by(usertag=usertag).first()

    # Returns True if the usertag is not in use
    return not bool(user)


def validate_login(usertag: str, password: str) -> bool:
    """Compare input password with the actual user hashed password.

    Parameters
    ----------
    usertag : `str`
        User  usertag

    password : `str`
        Password inserted in login form

    Return
    ------
    valid : `bool`
        Password matched or not
    """

    user = find_user(usertag)

    if user is None:
        return False

    return user.verify_password(password)


def user_suggestions(user: User, prof_owner: User, user_num: int) -> list:
    """Returns a mixed list of suggested users for the current user.

    Parameters
    ----------

    user : `User`
        The current user using the application

    prof_owner : `User`
        Owner of the current profile

    user_num : `int`
        How many users the function will return

    Notes
    -----
    If the total users number is lesser than `user_num`,
    a list containing all the users will be returned.
    """

    users = User.query.all()

    try:
        users = [u for u in users if not user.is_following(u)
                 and user != u != prof_owner]
    except AttributeError:
        # Current user is anonymous
        users = [u for u in users if u != prof_owner]

    if user_num <= len(users):
        return sample(users, user_num)

    # Less avaiable users than user_num required
    return sample(users, len(users))


@commit()
def register_user(username: str, usertag: str, password: str) -> User:
    """Register the user on the database and returns it

    Parameters
    ----------
    username : `str`
        Username

    usertag : `str`
        Usertag

    password : `str`
        User password

    Returns
    -------
    u : `User`
        Registered user instance
    """
    pic_num = randint(0, 1000)
    user_pic = f'https://avatars.dicebear.com/api/avataaars/{pic_num}.svg'

    u = User(username=username, usertag=usertag, profile_pic=user_pic)
    u.create_hashed_password(password)

    return u


@commit()
def create_quote(user: User, content: str) -> None:
    """Creates a quote linking it to it's author.

    Parameters
    ----------
    user : `User`
        Quote author

    quote_content : `str`
        String containing quote content
    """

    return Quote(content=content, user_id=user.id)
