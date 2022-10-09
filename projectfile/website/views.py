from flask import Blueprint,render_template, redirect, url_for, request, flash

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
    return render_template('account.html')

@bp.route('/test')
def test():
    return '<h1>test route<h1>'