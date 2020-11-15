from __future__ import annotations
from datetime import datetime

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin

from utils.decorators import commit
from exts import login
from exts import db


@login.user_loader
def load_user(id):
    return User.query.get(str(id))


# Association table
followers_table = db.Table("followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("user.id"))
)


class User(db.Model, UserMixin):
    """User table for database

    Notes
    -----
    One to many relationship with `Posts`.
    """

    # Table fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True)
    usertag = db.Column(db.String(20), index=True)
    profile_pic = db.Column(db.String(50))
    # For security reasons, only the hashed passwords are stored.
    password_hash = db.Column(db.String(128))

    # Using the Quote class as a column and referencing
    # the instance as "author" on the Quote object.
    _quotes = db.relationship("Quote", backref="author", lazy="dynamic")

    # Many-to-many relationship between users
    _following = db.relationship(
        "User",
        secondary=followers_table,
        primaryjoin=(followers_table.c.follower_id == id),
        secondaryjoin=(followers_table.c.followed_id == id),
        backref=db.backref("_followers", lazy="dynamic"),
        lazy="dynamic"
    )

    def create_hashed_password(self, password: str) -> str:
        """Generates a sha256 salted hash for user the password"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """
        Hashes the user input, compares it with the user hashed password
        and returns a boolean, whether the passwords match or not.
        """
        return check_password_hash(self.password_hash, password)

    def is_following(self, user: User) -> bool:
        return user in self._following

    @commit(add=False)
    def follow(self, user: User) -> None:

        if not self.is_following(user):
            self._following.append(user)

    @commit(add=False)
    def unfollow(self, user: User) -> None:

        if self.is_following(user):
            self._following.remove(user)

    @commit(add=False)
    def remove_quote(self, quote_id: int):
        quote = self._quotes.filter_by(id=quote_id).first()
        self._quotes.remove(quote)

    @property
    def quotes(self) -> list:
        return self._quotes.all()

    @property
    def following(self) -> list:
        return self._following.all()

    @property
    def followers(self) -> list:
        return self._followers.all()


class Quote(db.Model):
    """Quote table for database"""

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(150))

    timestamp = db.Column(db.DateTime,
                          index=True,
                          default=datetime.now)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("user.id"))

    @property
    def fmt_time(self):
        return self.timestamp.strftime("%B %d, %A %H:%M")
