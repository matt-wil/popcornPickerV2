import logging
from popcornPickerV2.datamanager.dataManagerABC import DataManagerInterface
from .models import User, Movie, db

# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Format
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Log to console
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
# Log to file
file_handler = logging.FileHandler("logs/app.logs")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class SQLiteDataManager(DataManagerInterface):
    """
    A class that implements the DataManagerInterface and provides an interface
    to interact with the SQLite database.

    This class provides methods to get all users, movies for a specific user,
    add a new user, add a new movie, update an existing movie, and delete a movie.

    The class uses the `flask_sqlalchemy` library to interact with the database.
    """

    def __init__(self, app):
        """
        Initialize the SQLite data manager.

        Args:
            app (Flask): The Flask application instance that we are a part of.
        """
        self.db = db
        with app.app_context():
            self.db.create_all()

    def get_all_users(self):
        """
        Retrieve all users from the database.

        Returns:
            list: A list of User objects if successful, otherwise an empty list.
        """
        try:
            return User.query.all()
        except Exception as e:
            print(f"Error fetching all users: {e}")
            logger.exception(f"Error fetching all users: {e}")
            return []

    def get_user_movies(self, user_id):
        """
        Retrieve movies for a specific user by user ID.

        Args:
            user_id (int): The ID of the user whose movies are to be fetched.

        Returns:
            list: A list of Movie objects if successful, otherwise an empty list.
        """
        try:
            return Movie.query.filter_by(user_id=user_id).all()
        except Exception as e:
            print(f"Error fetching movies for user {user_id}: {e}")
            logger.exception(f"Error fetching movies for user {user_id}: {e}")
            return []

    def add_user(self, user_name):
        """
        Add a new user to the database.

        Args:
            user_name (str): The name of the user to be added.

        Returns:
            User: The newly created User object if successful, otherwise None.
        """
        try:
            new_user = User(name=user_name)
            self.db.session.add(new_user)
            self.db.session.commit()
            return new_user
        except Exception as e:
            print(f"Error adding user: {e}")
            logger.exception(f"Error adding user: {e}")
            self.db.session.rollback()

    def add_movie(self, movie_data):
        """
        Add a new movie to the database.

        Args:
            movie_data (dict): A dictionary containing movie data.

        Returns:
            Movie: The newly created Movie object if successful, otherwise None.
        """
        try:
            new_movie = Movie(**movie_data)
            self.db.session.add(new_movie)
            self.db.session.commit()
            return new_movie
        except Exception as e:
            print(f"Error adding movie: {e}")
            logger.exception(f"Error adding movie: {e}")
            self.db.session.rollback()

    def update_movie(self, movie_id, updated_data):
        """
        Update an existing movie in the database.

        Args:
            movie_id (int): The ID of the movie to be updated.
            updated_data (dict): A dictionary containing updated movie data.

        Returns:
            Movie: The updated Movie object if successful, otherwise None.
        """
        try:
            movie = Movie.query.get(movie_id)
            if not movie:
                logger.error(f"Movie with ID {movie_id} not found.")
                print(f"Movie with ID {movie_id} not found.")
                return None
            for key, value in updated_data.items():
                setattr(movie, key, value)
            self.db.session.commit()
            return movie
        except Exception as e:
            print(f"Error updating movie: {e}")
            logger.exception(f"Error updating movie: {e}")
            self.db.session.rollback()

    def delete_movie(self, movie_id):
        """
        Delete a movie from the database.

        Args:
            movie_id (int): The ID of the movie to be deleted.

        Returns:
            bool: True if the movie was deleted successfully, otherwise False.
        """
        try:
            movie = Movie.query.get(movie_id)
            if not movie:
                print(f"Movie with ID {movie_id} not found.")
                return False
            self.db.session.delete(movie)
            self.db.session.commit()
            return True
        except Exception as e:
            print(f"Error deleting movie: {e}")
            logger.exception(f"Error deleting movie: {e}")
            self.db.session.rollback()
            return False
