from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    User model with a name and a one-to-many relationship to Movie.

    Attributes:
        id (int): Unique identifier for the user.
        name (str): The name of the user.
        movies (list[Movie]): The movies added by the user.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    # FOREIGN KEY REFERENCE
    movies = db.relationship('Movie', back_populates='user')


class Movie(db.Model):
    """
    Movie model representing a movie entry in the database with a relationship to a User.

    Attributes:
        id (int): Unique identifier for the movie.
        user_id (int): Identifier for the user who added the movie, references User.id.
        title (str): Title of the movie.
        director (str): Director of the movie.
        year (int): Release year of the movie.
        rating (float): Rating of the movie.
        img_url (str, optional): URL for the movie's image.
        link (str, optional): Link to more information about the movie.
        user (User): User object representing the owner of the movie.
    """
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    director = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String)
    link = db.Column(db.String)
    # FOREIGN KEY REFERENCE
    user = db.relationship('User', back_populates='movies')
