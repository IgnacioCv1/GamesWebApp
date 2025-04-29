from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User


def get_users(repo: AbstractRepository):
    return repo.get_users()


def get_user(username, repo: AbstractRepository):
    users = repo.get_users()
    for user in users:
        if username == user.username:
            return user


def password(user, repo: AbstractRepository):
    return repo.password(user)


def create_user(new_username, new_password, repo: AbstractRepository):
    new_user = User(new_username, new_password)
    repo.add_user(new_user)
