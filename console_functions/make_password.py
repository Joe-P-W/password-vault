import json
import random
from getpass import getpass

from crypto_files.vault_password_hasher import mask


def make_password():
    salt = random.randint(10**6, 10**7)
    while True:
        password = getpass("Set your password: ")
        check = getpass("Retype your password: ")
        if password == check:
            break
        else:
            print("Sorry what you typed did not match")

    with open("vault/vault_pass.json", "w") as in_file:
        _json = {
            "hash": mask(password, salt),
            "salt": salt
        }
        json.dump(_json, in_file)
