from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signin', methods = ['GET', 'POST'])
def sign_in():
    form = UserLoginForm()

    try:
        email = form.email.data
        password = form.password.data
        print(email, password)

        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash('Welcome to the Krusty Krab, home of the Krusty Krab. May I take your order?', 'auth-success')
            return redirect(url_for('site.home'))
        else:
            flash('No, this is Patrick', 'auth-failed')

    except:
        raise Exception('Invalid form data: Please check your form')

    return render_template('sign_in.html', form=form)

@auth.route('/signup', methods = ['GET', 'POST'])
def sign_up():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            user = User(email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'User-created')
            return redirect(url_for('site.home'))

    except:
        raise Exception('Invalid form data: Please check your form')

    return render_template('sign_up.html', form=form)

@auth.route('/logout')
def logout():
    return