from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, User, Review
from games.adapters.datareader.csvdatareader import read_csv_file
from typing import List


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__games = []
        self.__genres = []
        self.__users = []

    def add_game(self, game: Game):
        if isinstance(game, Game):
            self.__games.append(game)

    def search(self, target, filter):
        games = self.get_games()

        game_search_results = []

        for game in games:
            if filter == 'all' and target in game['game_title']:
                game_search_results.append(game)
            elif filter == 'genre' and target in game['game_genres']:
                game_search_results.append(game)
            elif filter == 'publisher' and target in game['game_publisher']:
                game_search_results.append(game)
            elif filter == 'developer' and target in game['game_publisher']:
                game_search_results.append(game)

        return game_search_results

    def get_games(self) -> List[Game]:
        games = self.__games

        game_dicts = []

        for game in games:

            genres_list = []
            for genre in game.genres:
                genres_list.append(genre.genre_name)

            game_dict = {
                'game_id': game.game_id,
                'game_title': game.title,
                'game_release': game.release_date,
                'game_img': game.image_url,
                'game_price': game.price,
                'game_des': game.description,
                'game_genres': genres_list,
                'game_publisher': game.publisher.publisher_name,
                'game_reviews': game.reviews

            }
            game_dicts.append(game_dict)

        return game_dicts


    def get_number_of_games(self):
        return len(self.__games)

    def add_user(self, newUser: User):
        if isinstance(newUser, User):
            self.__users.append(newUser)

    def get_users(self):
        return self.__users

    def get_genres(self):
        for game in self.__games:
            for genre in game.genres:
                if genre in self.__genres:
                    self.__genres[self.__genres.index(genre)].add_game(game)
                else:
                    genre.add_game(game)
                    self.__genres.append(genre)
        return self.__genres

    def get_game_by_title(self, game_title: str) -> Game:
        for game in self.__games:
            if game.title == game_title:

                genres_list = []
                for genre in game.genres:
                    genres_list.append(genre.genre_name)

                game_dict = {
                    'game_id': game.game_id,
                    'game_title': game.title,
                    'game_release': game.release_date,
                    'game_img': game.image_url,
                    'game_price': game.price,
                    'game_des': game.description,
                    'game_genres': genres_list,
                    'game_publisher': game.publisher.publisher_name,
                    'game_reviews': game.reviews

                }

                return game_dict

        return None

    def add_review_to_game_and_user(self, comment, game_name: str, rating: int, current_user: User):
        review_game = None
        for game in self.__games:
            if game.title == game_name:
                review_game = game

        for review in current_user.reviews:
            if review in review_game.reviews:
                return False

        review = Review(current_user, review_game, rating, comment)

        if review_game:
            review_game.add_review(review)
            current_user.add_review(review)
            return True

        return False

    def password(self, user: User):
        return user.password

    def append_wishlist(self, game_id, user, current_fav):
        current_game = None
        games = self.__games

        for game in games:
            if game.game_id == int(game_id):
                current_game = game
                break
        if current_game not in user.favorite_games and isinstance(current_game, Game):
            user.add_favourite_game(current_game)
            current_fav.append(current_game.game_id)
            return True
        return False

    def remove_favourite_game(self, user: User, game_id, current_fav):
        current_game = None

        for game in self.__games:
            if game.game_id == int(game_id):
                current_game = game
        if current_game in user.favorite_games:
            current_fav.remove(current_game.game_id)
            user.favorite_games.remove(current_game)
            return True
        return False



def memory_populate(repo: AbstractRepository):
    file_path = 'games/adapters/data/games.csv'
    csv_reader = GameFileCSVReader(file_path)

    csv_reader.read_csv_file()

    games = csv_reader.dataset_of_games

    for game in games:
        repo.add_game(game)