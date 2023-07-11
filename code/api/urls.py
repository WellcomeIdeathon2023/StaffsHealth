from App import App
from api import views

App.add_url_rule('/sms', 'sms', view_func=views.sms_reply, methods=["GET", "POST"])
