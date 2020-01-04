import random

from character_map.maps import maps


def generate_password() -> str:
    password = random.choice("1234567890") + random.choice("!\"£$%^&*-_=+")
    for i in range(random.randint(10, 20)):
        password += random.choice(maps[:90])

    random.shuffle(list(password))

    return "".join(password)