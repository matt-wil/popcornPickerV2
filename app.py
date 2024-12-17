# ___ FLASK FILE ___ #
from flask import Flask, render_template, redirect, request, url_for
from datamanager.models import db, User, Movie
from datamanager.sqliteDataManager import SQLiteDataManager, logger
from utilities import retrieve_all_movie_data

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

data_manager = SQLiteDataManager(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>', methods=['GET'])
def user_movies(user_id):
    users_movies = data_manager.get_user_movies(user_id=user_id)
    return render_template('user_movies.html', users_movies=users_movies, user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        data_manager.add_user(name)
        return redirect(url_for('home'))
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        movie_title = request.form['title']

        movie_info, movie_link = retrieve_all_movie_data(movie_title)
        if not movie_info or movie_info.get('Response') != 'True':
            logger.error(f"Failed to fetcha data for movie: {movie_title}")
            return "Failed to fetch movie data from OMDb API", 400

        existing_movies = data_manager.get_user_movies(user_id)
        if any(movie.title == movie_info['Title'] for movie in existing_movies):
            logger.warning(
                f"Movie '{movie_info['Title']}' already exists for user {user_id}.")
            return "Movie already exists in the list.", 400

        if movie_info['Response'] == 'True':
            movie_entry = {
                'title': movie_info['Title'],
                'year': movie_info['Year'],
                'director': movie_info['Director'],
                'rating': movie_info['imdbRating'],
                'img_url': movie_info['Poster'],
                'link': movie_link,
                'user_id': user_id
            }
            data_manager.add_movie(movie_entry)
            logger.info(
                f"Movie {movie_info['Title']} added successfully for user {user_id}")
            return redirect(url_for('user_movies', user_id=user_id))
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        key_list = ['title', 'year', 'rating', 'director']
        updated_data = {key: request.form[key]
                        for key in key_list if key in request.form}

        data_manager.update_movie(movie_id, updated_data=updated_data)
        return redirect(url_for('user_movies', user_id=user_id))

    movie = Movie.query.get(movie_id)
    if not movie or movie.user_id != user_id:
        return "Movie not found", 404
    return render_template('update_movie.html', movie=movie, user_id=user_id)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    success = data_manager.delete_movie(movie_id=movie_id)
    if not success:
        logger.error(f"Failed to delete movie: {movie_id}")
        return "Failed to delete movie", 400
    logger.info(f"Movie with ID {movie_id} deleted successfully.")
    return redirect(url_for('user_movies', user_id=user_id))


# error handling
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return render_template('405.html'), 405


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # with app.app_context():
    #     db.session.add(User(name="Matt"))
    #     db.session.add(User(name="Sabrina"))
    #     db.session.add(User(name="Wolfgang"))
    #     db.session.add(User(name="Magdalena"))
    #     db.session.commit()
    app.run(host="0.0.0.0", port=5002, debug=True)
