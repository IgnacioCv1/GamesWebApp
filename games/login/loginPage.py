from games.login import services

import games.adapters.repository as repo

from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from passlib.hash import pbkdf2_sha256
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from functools import wraps

login_blueprint = Blueprint('login_page', __name__)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # Gets user dictionary information
    users = services.get_users(repo.repo_instance)

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        current_user_obj = services.get_user(username, repo.repo_instance)

        if current_user_obj and pbkdf2_sha256.verify(password, services.password(current_user_obj, repo.repo_instance)):
            session['username'] = username
            session['favorites'] = []

            for game in current_user_obj.favorite_games:
                session['favorites'].append(game.game_id)

            return redirect(url_for('home_page'))
        else:
            flash('Login failed. Please check your credentials.', 'error')

    return render_template('loginSignup/loginPage.html', form=form)


@login_blueprint.route('/logout', methods=['POST'])
def logout():
    if 'username' in session:
        session.pop('username', None)
        session.pop('favorites', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login_page.login'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('login_page.login'))
        return view(**kwargs)
    return wrapped_view
