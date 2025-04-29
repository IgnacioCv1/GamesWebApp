import csv
import os

#from games.adapters import database_repository
from games.domainmodel.model import Genre, Game, Publisher

def read_csv_file(data_path, database_repository, database_mode, filename):
    if not os.path.exists(filename):
        print(f"path {filename} does not exist!")
        return
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                game_id = int(row["AppID"])
                title = row["Name"]
                game = Game(game_id, title)
                game.release_date = row["Release date"]
                game.price = float(row["Price"])
                game.description = row["About the game"]

                reviews = row["Reviews"].split(',')

                for review in reviews:
                    game.add_review(review)


                existing_publisher = database_repository.get_publisher_by_name(row["Publishers"].strip())
                if not existing_publisher:
                    publisher = Publisher(row["Publishers"])
                    database_repository.add_publisher(publisher)
                else:
                    publisher = existing_publisher

                game.publisher = publisher


                image_url = row["Header image"]
                game.image_url = image_url



                genre_names = row["Genres"].split(",")


                
                for genre_name in genre_names:
                    existing_genre = database_repository.get_genre_by_name(genre_name.strip())
                    if not existing_genre:
                        genre = Genre(genre_name.strip())
                        database_repository.add_genre(genre)
                    else:
                        genre = existing_genre


                    game.add_genre(genre)
                    genre.add_game(game)
                    database_repository.add_game(game)



            except ValueError as e:
                print(f"Skipping row due to invalid data: {e}")
            except KeyError as e:
                print(f"Skipping row due to missing key: {e}")

def read_csv_file_memory(mem_repository, filename):
    if not os.path.exists(filename):
        print(f"path {filename} does not exist!")
        return
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                game_id = int(row["AppID"])
                title = row["Name"]
                game = Game(game_id, title)
                game.release_date = row["Release date"]
                game.price = float(row["Price"])
                game.description = row["About the game"]

                reviews = row["Reviews"].split(',')

                for review in reviews:
                    game.add_review(review)



                publisher = Publisher(row["Publishers"])
                game.publisher = publisher

                image_url = row["Header image"]
                game.image_url = image_url

                genre_names = row["Genres"].split(",")

                for genre_name in genre_names:


                    genre = Genre(genre_name.strip())
                    game.add_genre(genre)
                    genre.add_game(game)


                mem_repository.add_game(game)



            except ValueError as e:
                print(f"Skipping row due to invalid data: {e}")
            except KeyError as e:
                print(f"Skipping row due to missing key: {e}")

    """@property
    def dataset_of_genres(self) -> set:
        return self.__dataset_of_genres
    def get_image_url(self):
        return self.__dataset_of_image_url

    def get_unique_games_count(self):
        return len(self.__dataset_of_games)

    def get_unique_publishers_count(self):
        return len(self.__dataset_of_publishers)

    @property
    def dataset_of_games(self) -> list:
        return self.__dataset_of_games

    @property
    def dataset_of_publishers(self) -> set:
        return self.__dataset_of_publishers

    @property
    def dataset_of_url(self) -> set:
        return self.__dataset_of_image_url
    """