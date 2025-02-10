import json

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

def get_all_user():
    return users

def get_user_by_id(id: int):
    for user in users:
        if user["id"] == id:
            return user
    return {"error": "User not found"}