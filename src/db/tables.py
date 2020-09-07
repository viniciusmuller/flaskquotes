from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model):
    """User table for database"""
 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True)
    usertag = db.Column(db.String(20), index=True)
    profile_pic = db.Column(db.String(50), index=True)
    password_hash = db.Column(db.String(128))
    quotes = db.relationship('Quote', backref='author', lazy='dynamic')

    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<User @{self.usertag}>'

    def create_hashed_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(uhash, password):
        return check_password_hash(uhash, password)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            db.session.commit()

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            db.session.commit()

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def remove_quote(self, quote):
        self.quotes.remove(quote)
        db.session.commit()

    def get_id(self):
        return str(self.id)

    @property
    def quotes_(self):
        return self.quotes.all()

    @property
    def total_following(self):
        return len(self.followed.all())

    @property
    def total_followers(self):
        return len(self.followers.all())

    # Flask login necessary properties
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False


class Quote(db.Model):
    """Quote table for database"""

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def str_time(self):
        return self.timestamp.strftime('%D %H:%M')

    def __repr__(self):
        return str(self.content)


db.create_all()
