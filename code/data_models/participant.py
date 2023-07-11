from App import App, DB as db
from utilities.parse_local_phone_number import parse_local_phone_number



class Participant(db.Model):
    __tablename__ = 'participant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    prefered_method = db.Column(db.String)

    def __init__(self, name, prefered_method):
        self.name = name
        self.prefered_method = prefered_method


class ParticipantTags(db.Model):
    __tablename__ = 'participantTags'
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer)
    tag = db.Column(db.String)

    def __init__(self, participant_id, tag):
        self.participant_id = participant_id
        self.tag = tag


class PhoneID(db.Model):
    __tablename__ = 'phoneId'
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer)
    contact_number = db.Column(db.String)
    preferred_method = db.Column(db.String)

    def __init__(self, participant_id, contact_number, preferred_method="phone"):
        self.participant_id = participant_id
        self.contact_number = parse_local_phone_number(contact_number)
        self.preferred_method = preferred_method


if __name__ == '__main__':

    with App.app_context():
        db.create_all()
