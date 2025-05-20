# Citation for the following program
# Date: 18 May 2025
# Code was adapted from the ZMQ Intro guide provided on the Canvas Assignment 4 page.
# URL to Canvas page: https://canvas.oregonstate.edu/courses/2024370/assignments/9998154?module_item_id=25330208
# URL to download the guide pdf: https://canvas.oregonstate.edu/courses/2024370/files/110412067?wrap=1

# favorites_microservice.py
import zmq
import json
import os

FILENAME = "favorites.json"

# Load existing favorites or create an empty list
if os.path.exists(FILENAME):
    with open(FILENAME, "r") as f:
        favorites = json.load(f)
else:
    favorites = []

# Setup ZMQ
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Favorites microservice is running on port 5555...")

while True:
    message = socket.recv_json()
    action = message.get("action")

    if action == "add":
        recipe = message.get("recipe")

        if not recipe or not isinstance(recipe, dict) or "title" not in recipe:
            socket.send_json({"response": "Invalid recipe format."})
            continue

        title = recipe["title"].strip().lower()

        # Check if a recipe with the same title already exists
        if any(r["title"].strip().lower() == title for r in favorites):
            response = f'"{recipe["title"]}" is already in your favorites list.'
        else:
            favorites.append(recipe)
            with open(FILENAME, "w") as f:
                json.dump(favorites, f, indent=2)
            response = f'"{recipe["title"]}" has been added to your favorites list!'

        socket.send_json({"response": response})

    elif action == "get":
        socket.send_json({"response": favorites})

    else:
        socket.send_json({"response": "Error: Invalid action."})
