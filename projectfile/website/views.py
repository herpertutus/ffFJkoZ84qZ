
from flask import Blueprint,render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .forms import CreateEventForm, LoginForm,RegisterForm
from werkzeug.security import generate_password_hash,check_password_hash

from .models import User, Event, Comment, Booking
from . import db

#gonna need to import models as we make them dont forget lads


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/events')
def allevents():
    return render_template('events.html')

@bp.route('/events/create')
def createEvent():
    form = CreateEventForm()
    return render_template('createevent.html', form=form)

@bp.route('/contact')
def contact():
    return render_template('contact.html')

@bp.route('/account', methods = ['GET', 'POST'])
def account():
    form = RegisterForm()
    if form.validate_on_submit():
        # max = db.session.query(func.max(User.id)).first()

        #get username, password and email from the form
        uname =form.username.data
        mail=form.email.data
        number=form.phnumber.data
        pwd = generate_password_hash(form.password.data)

        # new_user = User(username=uname, pwhash=pwd, email=mail, phnumber=number)
        thisuser = User.query.filter_by(id=f'{current_user.id}').first()
        print(thisuser)
        thisuser.username = uname
        thisuser.email = mail
        thisuser.pwhash = pwd
        thisuser.phnumber = number
        db.session.commit()

        flash("Updated info successfully")
        return redirect(url_for('main.account'))


    #this only should be accessed when user is logged in
    #needs: booking history
    return render_template('account.html', form=form)

@bp.route('/event/<eventid>', methods = ['GET', 'POST'])
def eventdetails(eventid):
    #attempt to find event in the database
    event = Event.query.filter_by(id=eventid).first()
    if type(event) == Event:
        owner = User.query.filter_by(id=event.ownerid).first()
        return render_template('eventdetails.html',imgurl=event.imgurl,
                                                   title=event.title,
                                                   description=event.description,
                                                   status=event.status,
                                                   datetime=event.datetime,
                                                   speaker=event.speaker,
                                                   creator=f"@{owner.username}",
                                                   tickets=event.tickets,
                                                   ticketprice=event.price)



    #render some sort of an error, no event found
    return render_template('eventdetails.html')


