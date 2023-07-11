from App import DB as db
from data_models.participant import Participant, PhoneID


def create_participant(name="", contact_method = "", phone_number=None):
    new_participant = Participant(name, contact_method)
    db.session.add(new_participant)
    db.session.commit()

    if phone_number:
        new_phone_id = PhoneID(new_participant.participant_id, phone_number)
        db.session.add(new_phone_id)
        db.session.commit()

    return new_participant
