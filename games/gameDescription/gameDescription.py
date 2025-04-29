from flask import Blueprint, render_template, session, request
from games.browseGames import services
import games.adapters.repository as repo
import math

# Config blueprint
description_blueprint = Blueprint('game_des', __name__)


@description_blueprint.route('/gameDescription/<string:game_title>', methods=['GET'])
def game_description(game_title):
    the_game = services.get_game_by_title(game_title, repo.repo_instance)

    if the_game is not None:
        session['last_viewed_game_name'] = game_title
        session['last_filter_requirement'] = 'all'

        stars = services.average_rating(game_title, repo.repo_instance)
        full_stars = int(stars[0])
        half_star = int(math.ceil(stars[1]))
        empty_stars = int(stars[2])
        avg_stars = stars[3]

        return render_template('gamesDescription.html', on_homepage=False, title='Games Library | Game Description', game=the_game, full_stars = full_stars, half_star=half_star, empty_stars=empty_stars, avg_stars=avg_stars)

