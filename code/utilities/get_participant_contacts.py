import pandas as pd
from App import DB as db

def alc_query_to_pandas(query, db=db):
    connection = db.session.connection()

    participant_contacts_sql = query.statement.compile(
        compile_kwargs={"literal_binds": True}
    )

    return pd.read_sql(participant_contacts_sql, connection)


def get_participant_contacts(name, scheduled_contacts, participant_generated_contacts,
                             messages):
    researcher_led_contacts = scheduled_contacts.query.\
        join(messages, scheduled_contacts.message_id == messages.id).\
        filter(scheduled_contacts.participant_id == name).\
        add_columns(messages.message)
    researcher_led_contacts_frame = alc_query_to_pandas(researcher_led_contacts, db)

    researcher_led_contacts_frame["Origin"] = "Care Team"

    participant_led_contacts = participant_generated_contacts.query.\
        join(messages, participant_generated_contacts.message_id == messages.id).\
        filter(participant_generated_contacts.participant_id == name).\
        add_columns(messages.message)
    participant_led_contacts_frame = alc_query_to_pandas(participant_led_contacts, db)

    participant_led_contacts_frame["Origin"] = "Participant"

    contacts_frame = pd.concat([
        researcher_led_contacts_frame, participant_led_contacts_frame
    ])

    contacts_frame = contacts_frame.sort_values("datetime", ascending=False).drop("id", axis=1)
    print(contacts_frame)

    contacts_frame_as_html = contacts_frame.to_html(classes='data', escape=False)
    return contacts_frame.columns.values, contacts_frame_as_html
