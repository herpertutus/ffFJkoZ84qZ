from cmath import log

from datetime import datetime
from functools import reduce
import os
import this
from unicodedata import category
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .forms import CreateEventForm, LoginForm, RegisterForm, PurchaseForm, CommentForm
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User, Event, Comment, Booking
from . import db

# gonna need to import models as we make them dont forget lads


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)


@bp.route('/events')
def allevents():
    events = Event.query.all()
    return render_template('events.html', events=events)


@bp.route('/events/create', methods=['GET', 'POST'])
@login_required
def createEvent():
    form = CreateEventForm()
    if form.validate_on_submit():
        # event form values
        eventName = form.name.data
        eventDescription = form.description.data
        eventDate = form.date.data
        eventCategory = form.category.data
        eventImage = form.image.data
        eventTickets = form.tickets.data
        eventPrice = form.price.data
        eventSpeaker = form.speaker.data
        eventStatus = form.status.data

        new_event = Event(ownerid=current_user.id,
                          imgurl=eventImage,
                          category=eventCategory,
                          title=eventName,
                          description=eventDescription,
                          speaker=eventSpeaker,
                          status=eventStatus,
                          datetime=eventDate,
                          tickets=eventTickets,
                          price=eventPrice)
        db.session.add(new_event)
        db.session.commit()
        print('event good')
        return redirect(url_for('main.allevents'))
    return render_template('createevent.html', form=form)

@bp.route('/update/<eventid>', methods=['GET', 'POST'])
@login_required
def updateEvent(eventid):
    events = Event.query.filter_by(id=eventid).first()
    form = CreateEventForm()
    if form.validate_on_submit():
            # event form values
            events.title = form.name.data
            events.description = form.description.data
            events.datetime = form.date.data
            events.category = form.category.data
            events.imgurl = form.image.data
            events.ticket = form.tickets.data
            events.price = form.price.data
            events.speaker = form.speaker.data
            events.status = form.status.data
            db.session.commit()
            return redirect(url_for('main.allevents'))
    return render_template('updateevent.html', form = form)

@bp.route('/contact')
def contact():
    return render_template('contact.html')


@bp.route('/account', methods=['GET', 'POST'])
def account():
    updateform = RegisterForm()
    bookings = Booking.query.filter_by(userid=current_user.id).all()
    events = Event.query.filter_by(ownerid=current_user.id).all()
    print(f"---{bookings}---")

    if updateform.validate_on_submit():
        # max = db.session.query(func.max(User.id)).first()

        # get username, password and email from the form
        uname = updateform.username.data
        mail = updateform.email.data
        number = updateform.phnumber.data
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

    return render_template('account.html', updateform=updateform, bookings=bookings, events=events)


@bp.route('/events/<eventid>', methods=['GET', 'POST'])
def eventdetails(eventid):
    # attempt to find event in the database
    event = Event.query.filter_by(id=eventid).first()

    if type(event) == Event:
        owner = User.query.filter_by(id=event.ownerid).first()
        # if(owner != current_user):
        #     return render_template('eventdetails.html')
        return render_template('eventdetails.html')

    # render some sort of an error, no event found
    # Stick if stuff here for comments
    form = CommentForm()
    comments = Event.query.filter_by(eventid=eventid).all()
    if form.validate_on_submit():
        # comment form values
        content1 = form.content.data
        commenttitle1 = form.commenttitle.data
        new_comments = comments(content1, commenttitle1)                   
        db.session.add(new_comments)
        db.session.commit()

    return render_template('eventdetails.html', imgurl=event.imgurl,
                               category=event.category,
                               speaker=event.speaker,
                               title=event.title,
                               description=event.description,
                               status=event.status,
                               datetime=event.datetime,
                               creator=f"@{owner.username}",
                               tickets=event.tickets,
                               ticketprice=event.price,
                               eventid=event.id)

@bp.route('/purchase/<eventid>', methods=['GET', 'POST'])
@login_required
def purchase(eventid):
    # attempt to find event in the database
    event = Event.query.filter_by(id=eventid).first()
   
    purchaseform = PurchaseForm()
    booked = False
    if purchaseform.validate_on_submit():
        purchedTix = purchaseform.tickets.data
        existingTix = event.tickets 
        
        if purchedTix > existingTix:
            
            
            booked = True

        new_purchase = Booking(userid=current_user.id,
                               eventid=eventid,
                               ticketprice=event.price,
                               qty=purchedTix,
                               date=event.datetime,
                               imgurl=event.imgurl,
                               title=event.title,
                               )
        
        finalTix =  existingTix - purchedTix
        
        thisevent = Event.query.filter_by(id=f'{eventid}').first()
        thisevent.tickets = finalTix

        if finalTix == 0:
            thisevent.status = "Booked Out"
            
                    
        if booked == False:
            db.session.add(new_purchase)
            db.session.commit()
            flash("Tickets Purchased Succesfuly, Refer to your order below")
            return redirect(url_for('main.account'))
        else:
            flash("Order quantity higher than available tickets")
        return redirect(url_for('main.account'))
    




        
    

    return render_template('purchase.html', 
                            form=purchaseform,imgurl=event.imgurl,
                            title=event.title,
                            description=event.description,
                            status=event.status,
                            datetime=event.datetime,
                            speaker=event.speaker,
                            tickets=event.tickets,
                            ticketprice=event.price)





    
    
