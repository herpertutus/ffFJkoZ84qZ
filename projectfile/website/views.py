from flask import Blueprint,render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

#gonna need to import models as we make them dont forget lads


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/events')
def allevents():
    return render_template('events.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html')

@bp.route('/account')
def account():
    #this only should be accessed when user is logged in
    #needs: booking history
    return render_template('account.html')

@bp.route('/test')
def test():
    return '<h1>test route<h1>'