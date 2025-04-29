from flask import Blueprint, render_template, request, session, redirect, url_for
from games.browseGames import services
import games.adapters.repository as repo
from games.login import services as login_services

add_fav_blueprint = Blueprint('add_fav', __name__)


@add_fav_blueprint.route('/add_fav', methods=['GET', 'POST'])
def add_favourite_game():
    current_game = None
    game_id = request.form.get('game_id')
    is_favorite = request.form.get('is_favorite')

    games = services.get_games(repo.repo_instance)
    for game in games:
        if game['game_id'] == game_id:
            current_game = game

    last_viewed_game_name = session.get('last_viewed_game_name')
    last_filter = session.get('last_filter_requirement')

    if game_id and is_favorite:
        if is_favorite == 'true':
            username = session['username']
            user = login_services.get_user(username, repo.repo_instance)
            services.remove_from_wishlist(user, game_id, repo.repo_instance)
            return redirect(url_for('game_des.game_description', game_title=last_viewed_game_name))
        elif is_favorite == 'false':
            username = session['username']
            user = login_services.get_user(username, repo.repo_instance)
            services.add_to_wishlist(user, game_id, repo.repo_instance)
            return redirect(url_for('game_des.game_description', game_title=last_viewed_game_name))

    return redirect(url_for('homePage'))  # Redirect back to your index route
