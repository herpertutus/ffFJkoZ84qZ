from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    pwhash = db.Column(db.String(255),unique=True, nullable=False)#should be 128 in length to store hash
    
    type = db.Column(db.String(20), nullable=False, default='guest')
    phnumber = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "<username: {}, id: {}>".format(self.username, self.id)