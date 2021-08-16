from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# user model. A model is like a table in a relational database. Inheret from the db.model class
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True) # id is the primary key
    username = db.Column(db.String(150),unique=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(256))
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    # this relationship connects each user to all of their posts
    posts = db.relationship("Post",backref="user",passive_deletes=True) # backref lets the user be referenced from the post ("post.user")
    comments = db.relationship("Comment",backref="user",passive_deletes=True)
    likes = db.relationship("Like",backref="user",passive_deletes=True)


class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.Text,nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    # for the author, the db.integer id must match an id from the User model. This makes sure that a post is
    # associated to a real user. If the user id is removed from the database, so are all his posts
    author = db.Column(db.Integer,db.ForeignKey("user.id",ondelete="cascade"),nullable=False) # inside the database, the User model is called "user"
    comments = db.relationship("Comment",backref="post",passive_deletes=True) # associate one post to many comments
    likes = db.relationship("Like",backref="post",passive_deletes=True)

class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.Text,nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    # for the author, the db.integer id must match an id from the User model. This makes sure that a post is
    # associated to a real user. If the user id is removed from the database, so are all his posts
    author = db.Column(db.Integer,db.ForeignKey("user.id",ondelete="cascade"),nullable=False) # inside the database, the User model is called "user"
    post_id = db.Column(db.Integer,db.ForeignKey("post.id",ondelete="CASCADE"),nullable=False)

class Like(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    author = db.Column(db.Integer,db.ForeignKey("user.id",ondelete="cascade"),nullable=False) # inside the database, the User model is called "user"
    post_id = db.Column(db.Integer,db.ForeignKey("post.id",ondelete="CASCADE"),nullable=False)
