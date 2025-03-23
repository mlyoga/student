import json

def authenticate_user(username, password):
    with open("data/users.json", "r") as f:
        users = json.load(f)
    return username in users and users[username] == password
