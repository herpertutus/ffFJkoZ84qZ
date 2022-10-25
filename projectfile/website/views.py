
from datetime import datetime
import os
from unicodedata import category
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
    events = Event.query.all()
    return render_template('events.html', events = events)

@bp.route('/events/create', methods = ['GET', 'POST'])
@login_required
def createEvent():
    form = CreateEventForm()
    if form.validate_on_submit():
        #event form values
        eventName = form.name.data
        eventDescription = form.description.data
        eventDate = form.date.data
        eventCategory = form.category.data
        eventImage = form.image.data
        eventTickets = form.tickets.data
        eventPrice = form.price.data
        eventStatus = form.status.data

        new_event = Event(imgurl = eventImage,
                          category = eventCategory,
                          title = eventName,
                          description = eventDescription,
                          status = eventStatus,
                          datetime = eventDate,
                          tickets = eventTickets,
                          price = eventPrice)
        db.session.add(new_event)
        db.session.commit()
        print('event good')
        return redirect(url_for('main.allevents'))
    return render_template('createevent.html', form=form)

@bp.route('/contact')
def contact():
    return render_template('contact.html')

@bp.route('/account', methods = ['GET', 'POST'])
def account():
    updateform = RegisterForm()
    bookings = Booking.query.filter_by(userid=current_user.id).all()
    print(f"---{bookings}---")

    if updateform.validate_on_submit():
        # max = db.session.query(func.max(User.id)).first()

        #get username, password and email from the form
        uname =updateform.username.data
        mail=updateform.email.data
        number=updateform.phnumber.data
        pwd = generate_password_hash(updateform.password.data)

        # new_user = User(username=uname, pwhash=pwd, email=mail, phnumber=number)
        thisuser = User.query.filter_by(id=f'{current_user.id}').first()
        thisuser.username = uname
        thisuser.email = mail
        thisuser.pwhash = pwd
        thisuser.phnumber = number
        db.session.commit()

        flash("Updated info successfully")
        return redirect(url_for('main.account'))

    return render_template('account.html', updateform=updateform, bookings=bookings)


@bp.route('/event/<eventid>', methods = ['GET', 'POST'])
def eventdetails(eventid):
    #attempt to find event in the database
    event = Event.query.filter_by(id=eventid).first()

    if type(event) == Event:
        owner = User.query.filter_by(id=event.ownerid).first()
        return render_template('eventdetails.html',imgurl=event.imgurl,
                                                   category = event.category,
                                                   title=event.title,
                                                   description=event.description,
                                                   status=event.status,
                                                   datetime=event.datetime,
                                                   tickets=event.tickets,
                                                   ticketprice=event.price)



    #render some sort of an error, no event found
    return render_template('eventdetails.html')


