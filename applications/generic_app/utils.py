import string
import random


def create_random_word(name_length=15):
    return "".join(
        random.choices(string.ascii_uppercase + string.digits, k=name_length)
    )
