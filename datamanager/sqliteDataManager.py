import logging
from popcornPickerV2.datamanager.dataManagerABC import DataManagerInterface
from .models import User, Movie, db

# Create a logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        self.db = db
        with app.app_context():
            self.db.create_all()

    def get_all_users(self):
        try:
            return User.query.all()
        except Exception as e:
            print(f"Error fetching all users: {e}")
            logger.exception(f"Error fetching all users: {e}")
            return []

    def get_user_movies(self, user_id):
        try:
            return Movie.query.filter_by(user_id=user_id).all()
        except Exception as e:
            print(f"Error fetching movies for user {user_id}: {e}")
            logger.exception(f"Error fetching movies for user {user_id}: {e}")
            return []

    def add_user(self, user_name):
        # V2 implement OAuth or proper database user/password system
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
        try:
            movie = Movie.query.get(movie_id)
            if not movie:
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
