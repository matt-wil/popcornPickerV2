from flask_sqlalchemy import SQLAlchemy
from popcornPickerV2.datamanager.dataManagerABC import DataManagerInterface


db = SQLAlchemy()


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.db = SQLAlchemy(db_file_name)
        self.User = self.db.Model.classes.User
        self.Movie = self.db.Model.classes.Movie

    def get_all_users(self):
        return self.db.session.query(self.User).all()

    def get_user_movies(self, user_id):
        return self.db.session.query(self.Movie).filter_by(user_id=user_id)

    def add_user(self, user_name):
        # implement later to add OAuth or proper database user/password system
        new_user = self.User(user_name)
        self.db.session.add(new_user)
        self.db.session.commit()

    def add_movie(self, movie_data):
        # movie data will be the necessary data from the movie class
        # ID, Title, Director, rating, year, image_link?
        new_movie = self.Movie(movie_data)
        self.db.session.add(movie_data)
        self.db.session.commit()

    def update_movie(self, movie_id, updated_data):
        # this will need to be implemented differently
        movie = self.db.session.query(self.Movie).get(movie_id)
        for key, value in updated_data.items():
            setattr(movie, key, value)
        self.db.session.commit()

    def delete_movie(self, movie_id):
        movie = self.db.session.query(self.Movie).get(movie_id)
        self.db.session.delete(movie)
        self.db.session.commit()


class User(db.Model):
    __tablename__: str = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

    movies = db.relationship('Movie', back_populates='user')


class Movie(db.Model):
    __tablename__: str = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String)
    director = db.Column(db.String)
    year = db.Column(db.Integer(4))
    rating = db.Column(db.Float)
    img_url = db.Column(db.String)

    user = db.relationship('User', back_populates='movies')
