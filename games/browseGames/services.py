import math

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Review, User
from flask import session


def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()

def get_game_by_title(game_title: str, repo: AbstractRepository):
    return repo.get_game_by_title(game_title)


def get_games(repo: AbstractRepository):
    return repo.get_games()


def search(target: str, filter: str, repo: AbstractRepository):
    search_results = repo.search(target, filter)

    return search_results



def get_genres(repo: AbstractRepository):
    return repo.get_genres()


def add_review_to_game_and_user(game_title: str, current_user: User, comment: str, rating: int,  repo: AbstractRepository):
    """
    games = repo.get_games()
    review_game = None
    for game in games:
        if game_title == game.title:
            review_game = game
            break

    for review in current_user.reviews:
        if review in review_game.reviews:
            return False

    review = Review(current_user, review_game, rating, comment)
    repo.add_review_to_game_and_user(review, review_game, current_user)

    """
    #game = repo.get_game_by_title(game_title)



    #review = Review(current_user, game, rating, comment)
    return repo.add_review_to_game_and_user(comment, game_title, rating, current_user)





def add_to_wishlist(user: User, game_id, repo: AbstractRepository):
    """
    current_game = None
    games = repo.get_games()
    for game in games:
        if game['game_id'] == int(game_id):
            current_game = game
    if current_game not in user.favorite_games and isinstance(current_game, Game):
        user.add_favourite_game(current_game)
        current_fav = session['favorites']
        current_fav.append(current_game.game_id)
        print(current_fav)
        print(current_game)
        """
    current_fav = session['favorites']
    if repo.append_wishlist(game_id, user, current_fav):
        session['favorites'] = current_fav



def remove_from_wishlist(user: User, game_id, repo: AbstractRepository):
    """
    current_game = None
    games = repo.get_games()
    for game in games:
        if game.game_id == int(game_id):
            current_game = game
    current_fav = session['favorites']
    current_fav.remove(current_game.game_id)
    session['favorites'] = current_fav
    """
    current_fav = session['favorites']
    if repo.remove_favourite_game(user, game_id, current_fav):
        session['favorites'] = current_fav


def average_rating(game_title, repo: AbstractRepository):
    the_game = repo.get_game_by_title(game_title)


    if len(the_game['game_reviews']) < 1:
        return [0, 0, 0, 0]

    avg_rating = 0
    count = 0.0
    for review in the_game['game_reviews']:
        count += 1
        avg_rating += review.rating

    avg_rating = avg_rating/count
    full_stars = math.floor(avg_rating)
    half_stars = avg_rating - full_stars
    empty_stars = math.floor(5-avg_rating)

    stars = [full_stars, half_stars, empty_stars, avg_rating]
    return stars

