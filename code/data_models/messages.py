from App import DB as db

class Message(db.Model):

    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)

    def __init__(self, message):
        self.message = message

class MessageTag(db.Model):

    __tablename__ = "messageTag"

    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer)
    tag = db.Column(db.String)

    def __init__(self, message_id, tag):
        self.message_id = message_id
        self.tag = tag
