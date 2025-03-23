# utils/database.py

import json
import os

DB_FILE = "achievements.json"  # File to store achievements

def save_achievement(username, category, details):
    """Save an achievement for a user."""
    data = load_data()
    if username not in data:
        data[username] = []
    data[username].append({"category": category, "details": details})
    save_data(data)

def get_achievements(username):
    """Retrieve achievements of a user."""
    data = load_data()
    return data.get(username, [])

def save_rating(username, rating):
    """Save a rating given by a user."""
    data = load_data("ratings.json")
    data[username] = rating
    save_data(data, "ratings.json")

def get_ratings():
    """Retrieve all ratings."""
    return load_data("ratings.json")

def load_data(filename=DB_FILE):
    """Load data from a JSON file."""
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as file:
        return json.load(file)

def save_data(data, filename=DB_FILE):
    """Save data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
