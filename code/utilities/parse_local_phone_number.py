import re

def parse_local_phone_number(phone_number, prefix="+44"):
    return re.sub("^0", prefix, phone_number)
