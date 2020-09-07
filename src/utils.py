import random

from db.tables import User, Quote
from app import db


def find_user(usersearch: str) -> User:
    """Search for a user either by name or tag and returns it
    
    Parameters
    ----------
    usersearch : `str`
        A username or usertag

    Return
    ------
    user : `User`
        Requested user instance
    """

    user = User.query.filter_by(usertag=usersearch).first() or \
           User.query.filter_by(username=usersearch).first()

    return user


def validate_signup(username: str) -> bool:
    """Checks if the user already exists before signup
    
    Parameter
    ---------
    username : `str`
        Username or usertag

    Return
    ------
    result : `bool`
        User already exists in the database
    """

    u = find_user(username)

    if not u:
        return True

    return False


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

    user_pic = f'https://api.adorable.io/avatars/200/{random.randint(0, 1000)}@adorable.io'

    u = User(username=username, usertag=usertag, profile_pic=user_pic)
    u.create_hashed_password(password)

    db.session.add(u)
    db.session.commit()
    return u


def validate_login(username: str, password: str) -> bool:
    """Compare form password with the actual user hashed password
    
    Parameters
    ----------
    username : `str`
        User username OR usertag
    
    password : `str`
        Password inserted in login form

    Return
    ------
    valid : `bool`
        Password matched or not
    """

    try:
        u = find_user(username)
        return User.check_password(u.password_hash, password)

    except: 
        return False


def user_suggestions(profile_owner: str, user_num: int) -> list:
    """Returns a list of suggested users with length given by 'user_num'.
    
    Tem q melhorar essa viu
    """
    users = User.query.all()
    profile_owner = find_user(profile_owner)

    if len(users) >= user_num:
        selected_users = random.sample(users, user_num)
        return selected_users


def create_quote(user: User, quote_content: str) -> None:
    """Creates a quote linking it to it's author
    
    Parameters
    ----------
    user : `User`
        Quote author

    quote_content : `str`
        String containing quote content
    """

    q = Quote(content=quote_content, user_id=user.id)
    db.session.add(q)
    db.session.commit()
