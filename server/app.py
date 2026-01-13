# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    """Return a JSON response with a welcome message."""
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)


@app.route('/demo_json')
def demo_json():
    """Return a JSON response with pet data using a dictionary."""
    pet_dict = {'id': 1,
                'name': 'Fido',
                'species': 'Dog'
                }
    return make_response(pet_dict, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
