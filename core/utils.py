import string
import random


def create_id():
    str = ''.join(random.choice(string.ascii_letters) for i in range(7))
    str = str.join(random.choice(string.digits) for i in range(3))
    return str
