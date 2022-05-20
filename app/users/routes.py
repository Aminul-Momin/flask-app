
from flask import Blueprint, url_for, redirect, flash, render_template, request
from flask_login import current_user, login_user, logout_user, login_required
#==============================================================================
from app import db, bcrypt
from app.users.forms import *
from app.users.utils import _save_piture, _send_reset_email
from app.models import User

users = Blueprint('users', __name__)
#==============================================================================

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data} !', 'success')
        return redirect(url_for('main.home'))

    return render_template('register.html', form=form, title='Register')


@users.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for('main.home')) if not next_page else redirect(next_page)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', form=form, title='Login')


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic_file = _save_piture(form.picture.data)
            current_user.image_file = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', form=form, image_file=image_file)



@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        _send_reset_email(user)
        flash("An email has been sent with instruction to reset your password", 'info')
        return redirect(url_for('users.login'))
    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash("This is an invalid or expired token", 'warning')
        return redirect(url_for('main.home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pass
        db.session.commit()
        flash('Your password has been updated', 'success')
        redirect(url_for('login'))

    return render_template("reset_password.html", title="Reset Password", form=form)
