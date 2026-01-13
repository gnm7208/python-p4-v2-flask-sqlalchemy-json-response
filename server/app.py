#!/usr/bin/env python3
"""
Flask Application for Pet Directory API.

This module provides a REST API for managing pet data,
with JSON responses for all endpoints.
"""

from flask import Flask, make_response
from flask_migrate import Migrate
from typing import Dict, List, Tuple, Any, Optional

from models import db, Pet

# Configure Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize database migrations
migrate = Migrate(app, db)
db.init_app(app)


@app.route('/', methods=['GET'])
def index() -> Tuple[Dict[str, str], int]:
    """
    Return a welcome message for the pet directory API.
    
    Returns:
        Tuple containing a welcome message dictionary and HTTP status code 200.
    
    Example Response:
        {
            "message": "Welcome to the pet directory!"
        }
    """
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)


@app.route('/pets/<int:id>', methods=['GET'])
def pet_by_id(id: int) -> Tuple[Dict[str, Any], int]:
    """
    Retrieve a pet by its ID.
    
    Args:
        id: The unique identifier of the pet to retrieve.
    
    Returns:
        Tuple containing the pet data dictionary and HTTP status code 200.
        Returns a 404 error if the pet is not found.
    
    Example Success Response:
        {
            "id": 1,
            "name": "Fido",
            "species": "Dog"
        }
    
    Example Error Response:
        {
            "error": "Pet not found"
        }
    
    Raises:
        404: If no pet with the given ID exists.
    """
    # Query the database for the pet by primary key
    pet = db.session.get(Pet, id)
    
    # Handle case where pet does not exist
    if not pet:
        return make_response({'error': 'Pet not found'}, 404)
    
    # Construct and return the response dictionary
    pet_dict = {
        'id': pet.id,
        'name': pet.name,
        'species': pet.species
    }
    return make_response(pet_dict, 200)


@app.route('/pets/species/<species>', methods=['GET'])
def pet_by_species(species: str) -> Tuple[List[Dict[str, Any]], int]:
    """
    Retrieve all pets filtered by species.
    
    Args:
        species: The species type to filter pets by (e.g., 'Dog', 'Cat').
    
    Returns:
        Tuple containing a list of pet dictionaries and HTTP status code 200.
        Returns a 404 error if no pets are found for the given species.
    
    Example Success Response:
        [
            {
                "id": 1,
                "name": "Buddy",
                "species": "Dog"
            },
            {
                "id": 3,
                "name": "Max",
                "species": "Dog"
            }
        ]
    
    Example Error Response:
        {
            "error": "No pets found for this species"
        }
    
    Raises:
        404: If no pets match the given species.
    """
    # Query the database for pets matching the specified species
    pets = Pet.query.filter_by(species=species).all()
    
    # Handle case where no pets are found for the species
    if not pets:
        return make_response({'error': 'No pets found for this species'}, 404)
    
    # Construct list of pet dictionaries from query results
    pets_list = [
        {
            'id': pet.id,
            'name': pet.name,
            'species': pet.species
        }
        for pet in pets
    ]
    return make_response(pets_list, 200)


if __name__ == '__main__':
    """
    Main entry point for running the Flask application.
    
    The application runs on port 5555 with debug mode enabled.
    """
    app.run(port=5555, debug=True)

