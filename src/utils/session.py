import random 

from utils.decorators import commit
from database.tables import User
from database.tables import Quote


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

    user = User.query.filter_by(usertag=usersearch).first() \
           or User.query.filter_by(username=usersearch).first()

    return user


# needs to find by usertag
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


# need to verify by usertag
def validate_login(usertag: str, password: str) -> bool:
    """Compare form password with the actual user hashed password
    
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

    return bool(user.check_password(password))


def user_suggestions(user: User, prof_owner: User, user_num: int) -> list:
    """Returns a list of suggested users with length given by 'user_num'.

    Tem q melhorar essa viu
    """

    users = User.query.all()

    try:
        users = [u for u in users if not user.is_following(u)
                 and user != u != prof_owner]
    # Current user is anonymous
    except AttributeError:
        pass

    if user_num <= len(users):
        return random.sample(users, user_num)

    # Less avaiable users than user_num required
    return random.sample(users, len(users))


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
    pic_num = random.randint(0, 1000)
    user_pic = f'https://api.adorable.io/avatars/200/{pic_num}@adorable.io'

    u = User(username=username, usertag=usertag, profile_pic=user_pic)
    u.create_hashed_password(password)

    return u


@commit()
def create_quote(user: User, content: str) -> None:
    """Creates a quote linking it to it's author
    
    Parameters
    ----------
    user : `User`
        Quote author

    quote_content : `str`
        String containing quote content
    """

    q = Quote(content=content, user_id=user.id)
    return q