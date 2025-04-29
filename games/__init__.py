"""Initialize Flask app."""

from pathlib import Path
from flask import Flask, render_template
#from games.adapters.datareader.csvdatareader import GameFileCSVReader
import games.adapters.repository as repo
from games.adapters import database_repository, repository_populate
from games.adapters.repository_populate import populate
from games.adapters.memory_repository import MemoryRepository, memory_populate
from games.domainmodel.model import Game
from games.adapters.orm import metadata, map_model_to_tables

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool


def create_app(test_config=None):
    """Construct the core application. """

    # Create the Flask app object.
    app = Flask(__name__)
    app.secret_key = '12345'

    app.config.from_object('config.Config')
    data_path = Path('games')/ 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        # Create MemoryRepo for a memory-based repo
        repo.repo_instance = MemoryRepository()
        database_mode = False
        # fill the repository from CSV file
        filename = 'games/adapters/data/games.csv'
        repository_populate.populate_mem_repo(data_path, repo.repo_instance, database_mode, filename)





    elif app.config['REPOSITORY'] == 'database':
        print("before")
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)
        print(len(database_engine.table_names()))

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("helloWorld")
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            database_mode = True
            filename = 'games/adapters/data/games.csv'

            repository_populate.populate(data_path, repo.repo_instance, database_mode, filename)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            print("else")
            map_model_to_tables()

        # implements the blueprints to the webpage
    with app.app_context():
        from .browseGames import browseGames
        app.register_blueprint(browseGames.browse_blueprint)

        from .gameDescription import gameDescription
        app.register_blueprint(gameDescription.description_blueprint)

        from games.adapters.SearchGames import Search
        app.register_blueprint(Search.search_blueprint)

        from .login import loginPage
        app.register_blueprint(loginPage.login_blueprint)

        from .signup import signupPage
        app.register_blueprint(signupPage.signup_blueprint)

        from .favourite_games import fav_games_funct
        app.register_blueprint(fav_games_funct.add_fav_blueprint)

        from .user_profile import user_profile
        app.register_blueprint(user_profile.user_profile_bp)

        # Register a callback the makes sure that database sessions are associated with http requests
        # We reset the session inside the database repository before a new flask request is generated
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.close_session()

    @app.route('/')
    def home_page_():
        return render_template('homePage.html', on_homepage=True)

    @app.route('/home_page')
    def home_page():
        return render_template('homePage.html', on_homepage=True)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
