import pywhatkit


def send_message(number, message):
    pywhatkit.sendwhatmsg_instantly(
        number, message,
        wait_time = 5, tab_close=True
    )
