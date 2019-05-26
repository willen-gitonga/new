from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Category(db.Model):
    '''
    define the different category objects
    '''
    __tablename__ = 'categories'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))


    def save_category(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_category(cls):
        category = Category.query.all()
        return category

class Pitch(db.Model):

    all_pitches = []

    __tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String(255))
    posted = db.Column(db.DateTime,default = datetime.utcnow)
    category_id = db.Column(db.Integer,db.ForeignKey("categories.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    Comment = db.relationship('Comment',backref='pitch',lazy="dynamic")

    def save_pitches(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitches(cls,id):
        Pitches = Pitch.query.filter_by(category_id = id).all()
        return Pitches

    '''
    list the pitches available
    '''


    

    @classmethod
    def clear_pitches(cls):
        Pitch.all_pitches.clear()



class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment_content = db.Column(db.String(255))
    user_id =db.Column(db.Integer,db.ForeignKey("users.id"))
    pitch_id = db.Column(db.Integer,db.ForeignKey("pitches.id"))





    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(pitch_id =id).all()
        return comments





class User(UserMixin,db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    pitches = db.relationship('Pitch',backref = 'user',lazy = "dynamic")
    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")
    pass_secure = db.Column(db.String(255))
    email = db.Column(db.String,unique=True,index=True)

    @property
    def password(self):
        raise AttributeError('you cannot read the password Attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure,password)



    def __repr__(self):
        return f'User {self.username}'
