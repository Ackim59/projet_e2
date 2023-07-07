from flask import render_template, Blueprint, url_for, redirect, flash
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user
from App.forms import LoginForm, SignUpForm
from App.models import db, User

auth = Blueprint("auth", __name__,template_folder="templates", static_folder="static")

@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data)[0]
        if user is not None:
            if user.verify_password(form.password.data):
                flash("Login scuccessfully!")
                login_user(user)
                return redirect(url_for('predict.predict'))
        else:
            flash("Email or password incorrect. Try again!")
    return render_template('login.html',form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if (form.validate_on_submit()):
        if (form.password.data==form.confirm_password.data):
            hashed_password = generate_password_hash(form.password.data)
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None:
                flash("This user already exists. Try again!")
                return render_template('signup.html',form=form)
            else:
                user = User(email=form.email.data, _hashed_password=hashed_password)
                db.session.add(user)
                db.session.commit()
                flash(f"User {form.email.data} added successfully!")
        else:
            flash("Passwords don't match. Try again!")
        form.email.data = ''
    return render_template("signup.html",form=form)

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    form = LoginForm()
    logout_user()
    return redirect(url_for('auth.login',form=form))
