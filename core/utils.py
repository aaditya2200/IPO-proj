import string
import random
from datetime import datetime


def create_id():
    str = ''.join(random.choice(string.ascii_letters) for i in range(7))
    str = str.join(random.choice(string.digits) for i in range(3))
    return str


def return_as_datetime_object(date):
    try:
        ipo_closing_date = datetime.strptime(date, '%b %d, %Y')
    except Exception as e:
        print('❌ Encountered exception ', e)
    return datetime.today(), ipo_closing_date
