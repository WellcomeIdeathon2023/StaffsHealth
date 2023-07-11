import pandas as pd

from data_models.contacts import ScheduledContact
from data_models.participant import PhoneID, Participant
from data_models.messages import Message

from datetime import datetime
from App import App, DB as db
from schedule import scheduler
from utilities.get_participant_contacts import alc_query_to_pandas
from collections import namedtuple
from twilio_api.twilio_send import send_sms

from utilities import whatsapp_msg


def get_messages_to_send(prefered_method="sms", scheduled_contacts=ScheduledContact):

    to_send_query = f""" 
        Select p.id as id, p.name as name, ph.contact_number as PhoneNumber, 
            m.message as message, sc.id as ContactID  
            from {scheduled_contacts.__tablename__} as sc 
            left join {Participant.__tablename__} as p on p.id = sc.participant_id
            left join {PhoneID.__tablename__} as ph on ph.participant_id = p.id
            left join {Message.__tablename__} as m on m.id = sc.message_id
            where (sc.delivered = false) and (ph.preferred_method = '{prefered_method}')     
    """

    jobs_frm = pd.read_sql_query(to_send_query, db.engine)

    return jobs_frm

def update_contacts_as_delivered(delivered_ids):
    session = db.session
    session.query(ScheduledContact).\
        filter(ScheduledContact.id.in_(delivered_ids)).\
        update({'delivered': True})

    session.commit()

def task_check_and_send(method, method_func):
    to_send_frm = get_messages_to_send(method)
    print(to_send_frm)
    for index, row in to_send_frm.iterrows():
        method_func(row.PhoneNumber, row.message)

    delivered_contact_ids = [int(i) for i in to_send_frm["ContactID"].values]
    update_contacts_as_delivered(delivered_contact_ids)

    print([i.delivered for i in ScheduledContact.query.all()])

def task_check_and_send_sms():
    task_check_and_send("sms", send_sms)

def task_check_and_send_whatsapp():
    task_check_and_send("whasapp", send_sms)
    # to_send_frm = get_messages_to_send()
    # for index, row in to_send_frm.iterrows():
    #     whatsapp_msg.send_message(row.number, row.message)
    #
    # delivered_contact_ids = [int(i) for i in to_send_frm["ContactID"].values]
    # update_contacts_as_delivered(delivered_contact_ids)
    #
    # print([i.delivered for i in ScheduledContact.query.all()])


if __name__ == '__main__':

    with App.app_context():
        # print([i.preferred_method for i in ScheduledContact.query.all()])
        print([i.preferred_method for i in PhoneID.query.all()])
        task_check_and_send_sms()
        # to_send_frm = get_messages_to_send()
        # print(to_send_frm)
        # for index, row in to_send_frm.iterrows():
        #     whatsapp_msg(row.WhatsAppNumber, row.message)
        #
        # delivered_contact_ids = [int(i) for i in to_send_frm["ContactID"].values]
        # update_contacts_as_delivered(delivered_contact_ids)
        #
        # print([i.delivered for i in ScheduledContact.query.all()])


# scheduler.start()
# print(scheduler.get_jobs())
# atexit.register(lambda: scheduler.shutdown())

