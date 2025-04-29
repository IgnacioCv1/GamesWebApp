from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Float, Text,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import mapper, relationship


from games.domainmodel.model import Publisher, Game, Genre, User, Review

metadata = MetaData()

publishers_table = Table('publishers', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, unique=True)

)

genres_table = Table('genres', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, unique=True)
)

games_table = Table('games', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String, unique=True),
    Column('price', Float),
    Column('release_date', String),
    Column('description', Text),
    Column('image_url', String),
    Column('website_url', String),
    Column('publisher_name', Integer, ForeignKey('publishers.name'))
)

game_genres_table = Table('game_genres', metadata,
    Column('id', Integer, primary_key=True),
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, unique=True),
    Column('password', String)
)

reviews_table = Table('reviews', metadata,
    Column('id', Integer, primary_key=True),
    Column('comment', Text),
    Column('rating', Integer),
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
    UniqueConstraint('game_id', 'user_id', name='uq_game_user')
)

favorite_games_table = Table('favorite_games', metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('game_id', Integer, ForeignKey('games.id'))
)


''' MAPPING THE CLASSES TO TABLES'''

def map_model_to_tables():
    # Publisher
    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name,
        '_Publisher__publisher_games': relationship(Game, back_populates='_Game__publisher')
    })

    # Genre
    mapper(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.name,
        '_Genre__games': relationship(Game, secondary=game_genres_table, back_populates='_Game__genres')
    })

    # Game
    mapper(Game, games_table, properties={
        '_Game__game_id': games_table.c.id,
        '_Game__game_title': games_table.c.title,
        '_Game__price': games_table.c.price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.description,
        '_Game__image_url': games_table.c.image_url,
        '_Game__website_url': games_table.c.website_url,
        '_Game__publisher': relationship(Publisher, back_populates='_Publisher__publisher_games'),
        '_Game__genres': relationship(Genre, secondary=game_genres_table, back_populates='_Genre__games'),
        '_Game__reviews': relationship(Review, back_populates='_Review__game')
    })

    # User
    mapper(User, users_table, properties={
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(Review, back_populates='_Review__user'),
        'favorite_games': relationship(Game, secondary=favorite_games_table, backref='favorited_by_users')
    })


    # Review
    mapper(Review, reviews_table, properties={
        '_Review__comment': reviews_table.c.comment,
        '_Review__rating': reviews_table.c.rating,
        '_Review__game': relationship(Game, back_populates='_Game__reviews'),
        '_Review__user': relationship(User, back_populates='_User__reviews'),

    })
