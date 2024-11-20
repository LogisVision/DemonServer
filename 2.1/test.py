from utils.firebase_handler import FirebaseHandler 

credential_path = "./data/logis_vision.json"
collection_name = "commands"

firebase_handler = FirebaseHandler(credential_path, collection_name)

command_id = "vA4JV7XOMzA8NJwO9KgQ"
firebase_handler.unlock_data("A", command_id)
