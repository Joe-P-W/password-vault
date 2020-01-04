import random

from character_map.maps import maps


def generate_password() -> str:
    password = ""
    for i in range(random.randint(10, 20)):
        password += random.choice(maps[:90])

    return password