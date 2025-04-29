from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from games.browseGames import services as browse_services
from games.login import services as login_services
import games.adapters.repository as repo
import math
from games.login.loginPage import login_required

search_blueprint = Blueprint('search_game', __name__)


@search_blueprint.route('/search-results', methods=['GET', 'POST'])
def search_results():
    """Posted search and return
       Rendering Search_results if valid."""
    if request.method == 'POST':
        target = request.form['search_query']
        filter_requirement = request.form.get('filter', 'all')
        return redirect(url_for('search_game.search_results', query=target, filter=filter_requirement))
    else:
        target = request.args.get('query')
        filter_requirement = request.args.get('filter')
        game_search_results = browse_services.search(target, filter_requirement, repo.repo_instance)


        if game_search_results:
            session['last_viewed_game_name'] = game_search_results[0]['game_title']
            session['last_filter_requirement'] = filter_requirement

            if filter_requirement == 'genre':

                return render_template('searchResults.html', title='Search Results',
                                       games=game_search_results, query=target,
                                       filter=filter_requirement)
            elif filter_requirement == 'publisher':
                return render_template('searchResults.html', title='Search Results',
                                       games=game_search_results, query=target,
                                       filter=filter_requirement)
            elif filter_requirement == 'all':
                return render_template('searchResults.html', title='Search Results',
                                       games=game_search_results, query=target,
                                       filter=filter_requirement)


        else:

            print("Search returned nothing!")
            return render_template('searchResults.html', title='Search Results',
                                   games=game_search_results, query=target,
                                   filter=filter_requirement)

    return render_template('homePage.html', on_homepage=True)


@search_blueprint.route('/add-comment/<string:game_title>', methods=['POST'])
@login_required
def add_comment(game_title):

    # Get User, Comment and Rating in order to add review to the game.
    current_user = session.get('username')
    comment = request.form['comment_content']
    rating = request.form['rating']
    # Finds User Object
    current_user_object = login_services.get_user(current_user, repo.repo_instance)

    # Gets data on the game name and filter the comment was made on, so that it can be searched again.
    last_viewed_game_name = session.get('last_viewed_game_name')
    last_filter = session.get('last_filter_requirement')

    # Checks if User has Review already. If not Creates review object then adds review to game and user objects review list.
    # Returns booleans on weather the user made Review already. False means User already Reviews this current game.
    if browse_services.add_review_to_game_and_user(game_title, current_user_object, comment, int(rating), repo.repo_instance):
        if last_viewed_game_name:
            return redirect(url_for('game_des.game_description', game_title=last_viewed_game_name))
        else:
            return redirect(url_for('home_page'))

    else:
        flash('You have already reviewed this game.', 'review_error')
        return redirect(url_for('game_des.game_description', game_title=last_viewed_game_name))






