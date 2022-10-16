import pwd
from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
) 
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required, logout_user
from . import db


#authentication blueprint
bp = Blueprint('auth', __name__)

@bp.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    error=None
    if(form.validate_on_submit()):
        usr = form.username.data
        pwd = form.password.data
        u1 = User.query.filter_by(username=usr).first() 
        if u1 is None:
            error='incorrect username'
        elif not check_password_hash(u1.pwhash, pwd):
            error='incorrect password'
        if error is None:
            login_user(u1)
            return redirect(url_for('main.index'))
        else:
            print(error)
            flash(error)

    return render_template('logintemp.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))