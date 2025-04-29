from flask import Blueprint, render_template, request,session
from games.browseGames import services
import games.adapters.repository as repo

# Config blue print
browse_blueprint = Blueprint('games_bp', __name__)


@browse_blueprint.route('/browseGames', methods = ['GET'])
def browse_games():
    # Removes game from session
    if 'game' in session:
        session.pop('game', None)

    total_games = services.get_number_of_games(repo.repo_instance)
    games = services.get_games(repo.repo_instance)
    genre_list = services.get_genres(repo.repo_instance)

    page = request.args.get('page', type=int, default=1)
    items_per_page = 15

    start = (page - 1) * items_per_page
    end = start + items_per_page
    paginated_games = games[start:end]

    total_pages = (total_games + items_per_page - 1) // items_per_page

    page_range = range(max(1, page - 2), min(total_pages, page + 2) + 1)

    return render_template('browsingGames/browseGames.html',
                           title = f"Browse Games | Game Library",
                           heading="Browse Games", games=paginated_games,
                           number_of_games=total_games,
                           total_pages=total_pages,
                           current_page=page,
                           page_range=page_range, on_homepage=False)