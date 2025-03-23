import json
import os
import threading

# Define file paths
ACHIEVEMENTS_FILE = "achievements.json"
RATINGS_FILE = "ratings.json"

# Lock to prevent concurrent write issues
lock = threading.Lock()

def save_achievement(username, category, details):
    """Save an achievement for a user."""
    data = load_data(ACHIEVEMENTS_FILE)
    if username not in data:
        data[username] = []
    data[username].append({"category": category, "details": details})
    save_data(data, ACHIEVEMENTS_FILE)

def get_achievements(username):
    """Retrieve achievements of a user."""
    data = load_data(ACHIEVEMENTS_FILE)
    return data.get(username, [])

def save_rating(username, rating):
    """Save a rating given by a user."""
    data = load_data(RATINGS_FILE)
    data[username] = rating
    save_data(data, RATINGS_FILE)

def get_ratings():
    """Retrieve all ratings."""
    return load_data(RATINGS_FILE)

def load_data(filename):
    """Load data from a JSON file safely. Creates file if missing."""
    if not os.path.exists(filename):
        save_data({}, filename)  # Create an empty file
        return {}

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"⚠️ Warning: {filename} is corrupted or missing. Resetting file.")
        save_data({}, filename)  # Reset file if corrupted
        return {}

def save_data(data, filename):
    """Safely save data to a JSON file using a lock."""
    with lock:
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"⚠️ Error saving data to {filename}: {e}")
