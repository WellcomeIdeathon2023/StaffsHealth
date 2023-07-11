from data_models.messages import Message
from App import DB as db

def add_message(message):
    new_msg = Message(message)
    db.session.add(new_msg)
    db.session.commit()
    return new_msg

