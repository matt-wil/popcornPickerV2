# ___ FLASK FILE ___ #
from flask import Flask
from datamanager.models import db
from datamanager.sqliteDataManager import SQLiteDataManager

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

data_manager = SQLiteDataManager(app)


@app.route('/', methods=['GET'])
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return str([user.name for user in users])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)


# with app.app_context():
#     db.session.add(User(name="Alice"))
#     db.session.add(User(name="Bob"))
#     db.session.commit()
