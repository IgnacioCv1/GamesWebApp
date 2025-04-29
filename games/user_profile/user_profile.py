from flask import Blueprint, render_template, request,session, url_for, redirect
import games.adapters.repository as repo
from games.login.loginPage import login_required
from games.login import services as login_services

# Config blue print
user_profile_bp = Blueprint('profile_bp', __name__)

@user_profile_bp.route('/user-profile/<string:username>', methods = ['GET'])
@login_required
def profile(username):
    if session['username'] != username:
        return redirect(url_for('home_page'))

    user = login_services.get_user(username, repo.repo_instance)
    reviews_list = user.reviews
    games_list = []
    for review in reviews_list:
        games_list.append(review.game)

    games_reviews_list = zip(games_list, reviews_list)
    fav_games = user.favorite_games

    return render_template('User-profile.html', username=username, games_reviews_list=games_reviews_list, fav_games=fav_games)
