from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, User, Genre, Publisher, Review
from typing import List


#from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from sqlalchemy.sql import text


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    """def add_games(self, games: List[Game]):
        with self._session_cm as scm:
            scm.session.add_all(games)
            scm.commit()"""

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:

            scm.session.add(genre)
            scm.commit()


    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.add(publisher)
            scm.commit()

    def add_game(self, game: Game):
        with self._session_cm as scm:
            if isinstance(game, Game):
                scm.session.add(game)
                scm.commit()

    def add_all_games(self, games):
        with self._session_cm as scm:
            scm.session.add_all(games)
            scm.commit()



    def get_genre_by_name(self, genre_name: str) -> Genre:
        with self._session_cm as scm:
            return scm.session.query(Genre).filter(Genre._Genre__genre_name==genre_name).first()

    def get_publisher_by_name(self, publisher_name: str):
        with self._session_cm as scm:
            return scm.session.query(Publisher).filter(Publisher._Publisher__publisher_name==publisher_name).first()



    def get_games(self) -> List[Game]:
        games = self._session_cm.session.query(Game).all()

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
        games = self._session_cm.session.query(Game).all()
        return len(games)

    def add_user(self, newUser: User):
        with self._session_cm as scm:
            if isinstance(newUser, User):
                scm.session.add(newUser)
                scm.commit()

    def search(self, target, filter):
        if filter == "all":
            games = self._session_cm.session.query(Game).filter(text(f"games.title like :target")).params(target=f"%{target}%").all()

        elif filter == "genre":

            genre = self._session_cm.session.query(Genre).filter(Genre._Genre__genre_name == target).all()
            if len(genre) < 1:
                return []
            games = genre[0].games

        elif filter == "publisher":
            games = self._session_cm.session.query(Game).filter(Game.publisher_name == target).all()


        else:
            games = []


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



    def get_users(self):
        users = self._session_cm.session.query(User).all()
        return users

    def get_genres(self):

        genres = self._session_cm.session.query(Genre).all()
        """
        for game in games:
            for genre in game.genres:
                if genre in genres:
                    genres[genres.index(genre)].add_game(game)
                else:
                    genre.add_game(game)
                    genres.append(genre)
        """
        return genres


    def get_game_by_title(self, game_title: str) -> Game:
        game = self._session_cm.session.query(Game).filter(Game._Game__game_title == game_title).first()

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


    def add_review_to_game_and_user(self, comment, game_name: str, rating: int, current_user: User):
        review_game = self._session_cm.session.query(Game).filter(Game._Game__game_title == game_name).first()
        for review in current_user.reviews:
            if review in review_game.reviews:
                return False
        review = Review(current_user, review_game, rating, comment)

        if review_game:
            review_game.add_review(review)
            current_user.add_review(review)
            with self._session_cm as scm:
                scm.session.add(review)
                scm.commit()
            return True

        return False


    def append_wishlist(self, game_id, user, current_fav):
        game = self._session_cm.session.query(Game).filter(Game._Game__game_id == game_id).first()
        if game not in user.favorite_games and isinstance(game, Game):
            user.add_favourite_game(game)
            current_fav.append(game.game_id)

            with self._session_cm as scm:
                scm.session.add(game)
                scm.commit()
                return True

        return False


    def remove_favourite_game(self, user: User, game_id, current_fav):
        game = self._session_cm.session.query(Game).filter(Game._Game__game_id == game_id).first()

        with self._session_cm as scm:
            if game in user.favorite_games:
                current_fav.remove(game.game_id)
                user.favorite_games.remove(game)
                scm.commit()
                return True
            else:
                return False
    def password(self, user: User):
        return user.password