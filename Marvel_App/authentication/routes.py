from flask import Blueprint, render_template
from Marvel_App.forms import UserLoginForm
from flask import request
from Marvel_App.models import db, User
from flask import redirect, url_for
from Marvel_App.models import check_password_hash
from flask import flash
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth',__name__,template_folder='auth_template')

@auth.route('/signup', methods=['GET','POST'])
def signup():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print([email, password]) # Testing data
        user = User(email, password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account, {email} has been created', 'create-success')
        return redirect(url_for('auth.signin'))
    return render_template('signup.html', form=form)

@auth.route('/signin', methods=['GET','POST'])
def signin():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print([email, password]) # Testing data 
        logged_user = User.query.filter(User.email == email).first()
        # authenticating someone:
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash(f'You have logged into, {email} successfully', 'auth-success')
            return redirect(url_for('site.home'))
        else:
            flash(f'Who are you?', 'auth-fail')
            return redirect(url_for('auth.signin'))
    return render_template('signin.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'You have logged out successfully', 'auth-success')
    return redirect(url_for('site.home'))

