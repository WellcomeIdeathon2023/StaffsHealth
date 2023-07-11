from App import App, DB as db
from data_models.participant import PhoneID
from utilities.create_participant import create_participant
from utilities.parse_local_phone_number import parse_local_phone_number


class ScheduledContact(db.Model):

    __tablename__ = 'scheduledContact'

    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    message_id = db.Column(db.Integer)
    delivered = db.Column(db.Boolean)

    def __init__(self, participant_id, datetime, message_id, delivered=False):
        self.participant_id = participant_id
        self.datetime = datetime
        self.message_id = message_id
        self.delivered = delivered

class ParticipantGeneratedContact(db.Model):

    __tablename__ = 'receivedContact'

    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    message_id = db.Column(db.Integer)
    responded_to = db.Column(db.Boolean)

    def __init__(self, participant_number, datetime, message_id):

        participant_number = parse_local_phone_number(participant_number)
        existing_participant = PhoneID.query.filter(PhoneID.contact_number == participant_number).first()

        if existing_participant:
            participant_id = existing_participant.participant_id
        else:
            new_participant = create_participant(phone_number=participant_number)
            participant_id = new_participant.participant_id

        self.participant_id = participant_id
        self.datetime = datetime
        self.message_id = message_id
        self.responded_to = False


if __name__ == '__main__':

    with App.app_context():
        db.create_all()
