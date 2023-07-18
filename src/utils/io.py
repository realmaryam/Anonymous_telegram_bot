import json
import pickle

DATA_DIR = "src/data/data.json"

def read_json(filename):
    with open(filename) as f:
        return json.load(f)


def write_json(data, filename, indent=4):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=indent)

def set_json_file(filename):
    with open(filename, 'w') as f:
        return json.dump([], f)

def update_user(message, filename):
    """ updates a user or add new user if do not exist
    parameters: 
    message_chat (telebot.message): the message that user have sended
    """
    with open(filename, 'r+') as f:
        users = json.load(f)
        
        user_found = False
        for user in users:
            if user['id'] == id:
                user['text'] = message.text
                user_found = True
                return
        
        if (not users) or (not user_found):
            new_user = {
                "id": message.chat.id,
                "first_name": message.chat.first_name,
                "username": message.chat.username,
                "text": message.text,
                "state": None,
                "connected_to": None
            }
            users.append(new_user)
            json.dump(users, f)
  
    





# def set_pickle_file(filename):
#     with open(filename, 'wb') as f:
#         return pickle.dump(None, f)

# def read_pickle(filename):
#     with open(filename, 'rb') as f:
#         return pickle.load(f)

# def write_pickle(data, filename):
#     with open(filename, 'ab') as f:
#         pickle.dump(data, f)


