import abc
from typing import List

from games.domainmodel.model import Game

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message = None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_game(self, game: Game):
        """ Add a game to the repository list of games """
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        """ Returns list of games """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self):
        """ Unsure if we need to implement this. What is the use case?"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_users(self):
        """ Returns dictionary of registered users """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, newUser):
        """ Adds new User Objects to Object list """
        raise NotImplementedError

    @abc.abstractmethod
    def password(self, user):
        """ Returns User Object Password """
        raise NotImplementedError

