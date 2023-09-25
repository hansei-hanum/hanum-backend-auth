import random
import string


def random_string(length):
    characters = string.ascii_letters + string.digits

    random_chars = random.sample(characters, length - 1)
    random_chars.append(random.choice(string.ascii_letters))
    random_chars.append(random.choice(string.digits))

    random.shuffle(random_chars)
    random_string = "".join(random_chars)
    return random_string


def random_number(length):
    numbers = string.digits

    random_nums = random.sample(numbers, length)
    random_string = "".join(random_nums)
    return random_string
