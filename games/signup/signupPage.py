from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from games.login import services
import games.adapters.repository as repo
from passlib.hash import pbkdf2_sha256
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

signup_blueprint = Blueprint('signup_page', __name__)


class SignupForm(FlaskForm):
    # Created sign up form
    new_username = StringField('New Username', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Sign Up')


@signup_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    # Get user dictionary information - uses services from loginPage
    users = services.get_users(repo.repo_instance)

    form = SignupForm()
    if form.validate_on_submit():
        new_username = form.new_username.data
        new_password = form.new_password.data

        username_list = [user.username for user in users]

        if new_username in username_list:
            flash('Username already taken!', 'error')
        else:
            # Create User Object and Adds new user to repo
            services.create_user(new_username, pbkdf2_sha256.hash(new_password), repo.repo_instance)

            # old method of adding users
            # users[new_username] = {'password_hash': pbkdf2_sha256.hash(new_password)}

            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login_page.login'))

    return render_template('loginSignup/signupPage.html', form=form)