import flask
from flask import request
from App import App, csrf, DB as db
from data_models.messages import Message, MessageTag
from data_models.contacts import ParticipantGeneratedContact
from datetime import datetime
from utilities.get_participant_contacts import alc_query_to_pandas

@csrf.exempt
def sms_reply():
    if request.method == "POST":

        body = request.form.getlist("Body")[0]
        participant_number = request.form.getlist("From")[0]
        print(participant_number)
        new_message = Message(body)
        db.session.add(new_message)
        db.session.commit()

        tagset = ["Received"]

        if "help" in body.lower():
            tagset += ["Warning"]

        for tag in tagset:
            new_msg_tag = MessageTag(new_message.id, tag)
            db.session.add(new_msg_tag)
            db.session.commit()

        new_contact = ParticipantGeneratedContact(participant_number, datetime.now(), new_message.id)
        db.session.add(new_contact)
        db.session.commit()

        print(request.form.getlist("Body"))
        print(request.form)
        return "Bob"

    return "Hello World 2"

def get_message_tags(message_id):

    message_tags = MessageTag.query.filter(MessageTag.message_id == int(message_id)).all()

    return [i.tag for i in message_tags]


def prepare_message_tags(key, class_dict, initial_tag = "message-tag-row"):
    tag_list = class_dict.get(key, [])
    message_tag_list = [initial_tag]

    for i in tag_list:
        print("Tag with", i)
        message_tag_list.append(f"message-tag-{i.lower()}")

    return " ".join(message_tag_list)

def to_html_row(index, values):
    row = [f"<th>{index}</th>"]
    [row.append(f"<td>{i}</td>") for i in values]
    return "\n".join(row)


def to_html_body(frame, class_dict):
    html_rows = [to_html_row(index, row.values) for index, row in frame.iterrows()]
    print(frame.index)
    class_rows = [prepare_message_tags(i, class_dict) for i in frame.index]

    print("in html body: ", class_rows)

    html_table = [f"<tr class='{tr_class}'>{row}</tr> " for tr_class, row in zip(class_rows, html_rows)]

    body = "<tbody>" + "\n".join(html_table) + "</tbody>"
    return body


def to_html_head(frame):
    table_header = [f"<th></th>"]
    for i in frame.columns:
        table_header.append(f"<th>{i}</th>")

    table_header = "\n".join(table_header)
    table_header = f"<tr style='text-align: right;'> {table_header} </tr> "

    return f"<thead> {table_header} </thead>"


def to_html_table(frame, class_dict):
    return "<table border='1' class='dataframe data'>" + \
           to_html_head(frame) + \
           to_html_body(frame, class_dict) + \
           "</table>"

def unanswered_messages():
    query = ParticipantGeneratedContact.query\
        .join(Message, Message.id == ParticipantGeneratedContact.message_id)\
        .filter(ParticipantGeneratedContact.responded_to == False)\
        .add_columns(Message.message)

    message_frame = alc_query_to_pandas(query, db)

    message_tag_classes = {i: get_message_tags(i) for i in message_frame["message_id"].values}
    print(message_tag_classes)
    message_frame["participant_id"] = [f'<a href = "/crm/{i}"> {i} </a>' for i in message_frame["id"].values]
    message_frame.index = message_frame["message_id"]

    message_frame_as_html = to_html_table(message_frame, message_tag_classes)

    return flask.render_template("unanswered_messages.html",
                                 message_tables=[message_frame_as_html], message_titles=message_frame.columns.values)
