# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import flask
from flask import request, jsonify
import pandas as pd
import datetime as dt, time

# from schedule import schedulers
from sqlalchemy import select

from App import App, DB as db, csrf
from forms.register_form import RegisterForm
from forms.add_tag_form import AddTagForm
from forms.add_contact_form import AddContactForm
from utilities.get_participant_contacts import get_participant_contacts, alc_query_to_pandas

from data_models.participant import Participant, ParticipantTags, PhoneID
from data_models.contacts import ScheduledContact, ParticipantGeneratedContact
from utilities.message_handlers import add_message, Message

from api import views
from pyngrok import ngrok



@App.route("/")
def index():
    return flask.render_template("index.html")


@App.route("/crm")
def crm():

    frm = pd.read_sql_query(
        sql=db.select(
            Participant.id,
            Participant.name
        ),
        con=db.engine
    )

    frm["Link"] = [f'<a href = "/crm/{i}"> {i} </a>' for i in frm["id"].values]

    frm_as_html = frm.to_html(classes='data', escape=False)

    return flask.render_template("crm.html",
                                 tables=[frm_as_html], titles=frm.columns.values)


@App.route("/crm/<name>", methods=['GET', 'POST'])
def participant(name):
    participant = Participant.query.filter(Participant.id == name).first()
    participant_tags = ParticipantTags.query.filter(ParticipantTags.participant_id == name).all()
    contacts_titles, contacts_table = get_participant_contacts(name, ScheduledContact,
                                                               ParticipantGeneratedContact, Message)

    current_tags = set([i.tag for i in participant_tags])

    add_tag_form = AddTagForm()
    add_contact_form = AddContactForm()

    add_contact_form.time.data = dt.time(12, 0, 0)

    if add_tag_form.submit_AddTagForm.data and add_tag_form.validate_on_submit():
        tag = request.form["tag"]
        new_participant_tag = ParticipantTags(name, tag)

        db.session.add(new_participant_tag)
        db.session.commit()

        current_tags.add(tag)

        return flask.render_template('participant.html', name=name, participant=participant,
                                 form=add_tag_form, tags=current_tags,
                                 add_contact_form=add_contact_form,
                                 contacts_tables=[contacts_table],
                                 contacts_titles=contacts_titles
        )

    if add_contact_form.submit_AddContactForm.data and add_contact_form.validate_on_submit():
        date = request.form["date"]
        time = request.form["time"]

        message = request.form["message"]
        new_msg = add_message(message)

        datetime_str = f"{date} {time}"
        datetime = dt.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

        new_scheduled_contact = ScheduledContact(name, datetime, new_msg.id)

        db.session.add(new_scheduled_contact)
        db.session.commit()

        contacts_titles, contacts_table = get_participant_contacts(name, ScheduledContact)

        return flask.render_template('participant.html', name=name, participant=participant,
                                     form=add_tag_form, tags=current_tags,
                                     add_contact_form=add_contact_form,
                                     contacts_tables=[contacts_table],
                                     contacts_titles=contacts_titles
                                     )

    return flask.render_template('participant.html', name=name, participant=participant,
                                 form=add_tag_form, tags=current_tags,
                                 add_contact_form=add_contact_form,
                                 contacts_tables=[contacts_table],
                                 contacts_titles=contacts_titles
                                 )


@App.route("/message")
def message():
    all_messages = Message.query

    message_frame = alc_query_to_pandas(all_messages, db)
    message_frame["Link"] = [f'<a href = "/message/{i}"> {i} </a>' for i in message_frame["id"].values]

    message_frame_as_html = message_frame.to_html(classes='data', escape=False)

    return flask.render_template("messages.html",
                                 tables=[message_frame_as_html], titles=message_frame.columns.values)


@App.route("/message/<job_id>")
def job(job_id):

    print(int(job_id))

    message = Message.query.filter(Message.id == int(job_id)).one()
    print(message.id)

    AddContactForm

    return flask.render_template("individual_message.html", message=message)


contact_dict = dict(WhatsApp = PhoneID, Phone=PhoneID)


@App.route("/register_participant", methods=['GET', 'POST'])
def register_participant():
    registration_form = RegisterForm()

    if registration_form.validate_on_submit():
        name = request.form["name"]
        contact_method = request.form["contact_method"]
        contact_number = request.form["phone_number"]

        new_participant = Participant(name, contact_method)
        db.session.add(new_participant)
        db.session.commit()

        contact_method_class = contact_dict.get(contact_method, None)

        if contact_method_class:
            new_contact = contact_method_class(new_participant.id, contact_number)
            db.session.add(new_contact)
            db.session.commit()

        else:
            print(f"Contact method: {contact_method} not implemented.")

        message = f"The data for participant {name} has been submitted."

        flask.flash(message)

        return flask.redirect(flask.url_for('register_participant'))

    return flask.render_template("register_participant.html", form=registration_form)

@App.route("/send_to_tag/")
def send_to_tag_index():
    tagset = select(ParticipantTags.tag).distinct()
    tagset = db.session.execute(tagset)
    tagset = [i[0] for i in tagset.fetchall()]
    print(tagset)
    return flask.render_template("participant_tags.html", tagset=tagset)


@App.route("/send_to_tag/<tag>", methods=['GET', 'POST'])
def send_to_tag(tag):
    new_contact = AddContactForm()
    new_contact.time.data = dt.time(12, 0, 0)
    if new_contact.validate_on_submit():

        date = request.form["date"]
        time = request.form["time"]

        form_message = request.form["message"]
        new_msg = add_message(form_message)

        datetime_str = f"{date} {time}"
        form_datetime = dt.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

        tagged = ParticipantTags.query.filter(ParticipantTags.tag == tag).all()
        to_add = [i.participant_id for i in tagged]

        for _id in to_add:
            sc = ScheduledContact(_id, form_datetime, new_msg.id)
            db.session.add(sc)
            db.session.commit()

        n = len(to_add)
        flash_message = f"New contacts planned for {n} participants tagged with {tag}."
        flask.flash(flash_message)

        return flask.redirect(flask.url_for("send_to_tag", tag=tag))

    return flask.render_template("message_by_tag.html", tag=tag,
                                 add_contact_form=new_contact)


App.add_url_rule('/sms', 'sms_reply', view_func=views.sms_reply, methods=["GET", "POST"])
App.add_url_rule('/unanswered_messages', 'unanswered_messages', view_func=views.unanswered_messages)



if __name__ == "__main__":
    App.debug = True
    App.run()
