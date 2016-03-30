import random
import uuid


def random_word():
    return str(uuid.uuid4())


def random_number():
    return random.choice(range(0, 10000))
