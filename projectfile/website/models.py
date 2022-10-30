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
        return f"<username: {self.username}, id: {self.id}>"

class Booking(db.Model):
    __tablename__='bookings'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    eventid = db.Column(db.Integer)
    ticketprice = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    date = db.Column(db.String(20), nullable=False)
    imgurl = db.Column(db.String(200), index=True)
    title = db.Column(db.String(40), index=True)

    def __repr__(self):
        return f"<id: {self.id}, date: {self.date}>"

class Event(db.Model):
    __tablename__='events'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False, default='Unpublished')
    datetime = db.Column(db.String(30), index=True)
    speaker = db.Column(db.String(40), index=True)
    ownerid = db.Column(db.Integer)
    tickets = db.Column(db.Integer)
    price = db.Column(db.Integer)
    title = db.Column(db.String(40), index=True)
    description = db.Column(db.String(550), index=True)
    category = db.Column(db.String(40), index=True)
    imgurl = db.Column(db.String(200), index=True)

    def __repr__(self):
        return f"<id: {self.id}, title: {self.title}>"

class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer, primary_key=True)
    commenterid = db.Column(db.Integer)
    commentername = db.Column(db.String(40))
    content = db.Column(db.String(550), index=True)
    date = db.Column(db.String(30), index=True)

    def __repr__(self):
        return f"<id: {self.id}, commentername: {self.commentername}>"

