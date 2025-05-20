# Overview
This microservice runs locally and allows a client application to manage a persistent list of favorite recipes. It supports adding a recipe (while preventing duplicates) and retrieving the current list of favorite recipes. It communicates using JSON messages over a ZeroMQ REQ/REP socket.
## How to Programmatically Request Data
1. Connect to the ZMQ socket for the microservice.
```python
import zmq
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
```
2. Format the data to send using the following format:
```python
message = {
    "action": "add",              # or "get"
    "recipe_name": "Chicken Tacos"   # only needed for "add" action
}
```
3. Use socket.send_json() to send the message.
```python
message = {
    "action": "get"
}
socket.send_json(message)
```
4. To retrieve your current favorites, use the following format:
```python
message = {
    "action": "get"
}
socket.send_json(message)
```
## Example Call: Add a Recipe to Favorites
```python
message = {
    "action": "add",
    "recipe_name": "Chicken Tacos"
}
socket.send_json(message)
response = socket.recv_json()
print(response["response"])  # "Chicken Tacos has been added to your favorites list!"
```
## Example Call: Get Favorite Recipes
```python
message = {
    "action": "get"
}
socket.send_json(message)
response = socket.recv_json()
print(response["response"])  # ["Chicken Tacos"]
```
## How to Programmatically Receive Data
1. Stay connected to the socket.
2. Receive data using socket.recv_json().
3. The server will return a dictionary with a response field.
If the action is "get", the response will be a list of recipe names.
If the action is "add", the response will be a confirmation message.
## Example Function: Add and Retrieve Favorites
```python
def add_recipe_to_favorites(recipe_name):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    message = {"action": "add", "recipe_name": recipe_name}
    socket.send_json(message)
    return socket.recv_json()["response"]

def get_favorites():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    message = {"action": "get"}
    socket.send_json(message)
    return socket.recv_json()["response"]

# Example usage
print(add_recipe_to_favorites("Pasta Carbonara"))
print(get_favorites())
```
## Mitigation Plan:
A.	Teammate for Microservice A: Adrianna Hoffman

B.	Current Status: Microservice is fully implemented. All features (adding favorites, preventing duplicates, persisting favorites) are working as expected.

C.	How Teammate Will Access Microservice:

  	1. Users will get the code from the GitHub repository.
   
	2. [GitHub repo](https://github.com/Ecraindrop/CS-361-Microservice.git)
   
  	3. Users will run the microservice locally and import it into their Main Program.
   
D.	What to Do If There Are Issues:
  	If users cannot access the microservice or runs into issues with function calls, they can contact me via Discord or Teams.
  	My availability for troubleshooting is between 3 PM - 9 PM (weekdays).
   
E.	Deadline for Reporting Issues: users should report any access issues by Friday, May 23th, 2025.

F.	Additional Notes:
The microservice relies on a JSON file for persistent storage. If there are file access issues, ensure the program has the right permissions.

## UML Diagram

