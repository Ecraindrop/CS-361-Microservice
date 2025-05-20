# Citation for the following program
# Date: 18 May 2025
# Code was adapted from the ZMQ Intro guide provided on the Canvas Assignment 4 page.
# URL to Canvas page: https://canvas.oregonstate.edu/courses/2024370/assignments/9998154?module_item_id=25330208
# URL to download the guide pdf: https://canvas.oregonstate.edu/courses/2024370/files/110412067?wrap=1

import zmq
import json


def load_recipes(filename="recipes.json"):
    with open(filename, "r") as f:
        return json.load(f)
    

def add_recipe(recipe):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    
    message = {
        "action": "add",
        "recipe": recipe
    }
    
    socket.send_json(message)
    response = socket.recv_json()
    print(response["response"])


def get_favorites():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    
    message = {"action": "get"}
    socket.send_json(message)
    response = socket.recv_json()

    print("\nFavorite Recipes:")
    for i, recipe in enumerate(response["response"], 1):
        print(f"{i}. {recipe['title']}")


if __name__ == "__main__":
    recipes = load_recipes()

    while True:
        print("\n--- Favorite Recipes CLI ---")
        print("1. Add recipe to favorites")
        print("2. Show favorite recipes")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            for i, r in enumerate(recipes, 1):
                print(f"{i}. {r['title']}")
            index = input("Select recipe number to add: ").strip()
            if index.isdigit() and 1 <= int(index) <= len(recipes):
                add_recipe(recipes[int(index) - 1])
            else:
                print("Invalid selection.")
        elif choice == "2":
            get_favorites()
        elif choice == "3":
            print("Exiting.")
            break
        else:
            print("Invalid choice.")
