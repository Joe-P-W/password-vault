import json
from getpass import getpass
import random

from crypto_files.encode import encode_pass
from console_functions.get_vault_password import get_vault_password


def enter_password_to_vault():
    salt = get_vault_password()

    site = input("What is this for? ")
    user = input("Username? ")
    while True:
        password = getpass("Set your password: ")
        check = getpass("Retype your password: ")
        if password == check:
            break
        else:
            print("\nSorry what you typed did not match try again: ")

    with open("vault/passwords.json", "r") as in_file:
        _json = json.load(in_file)

    num = random.randint(1, 2)

    if num == 1:
        _json[encode_pass(site, salt)] = {
            encode_pass("Username", salt): encode_pass(user, salt),
            encode_pass("Password", salt): encode_pass(password, salt)
        }

    else:
        _json[encode_pass(site, salt)] = {
            encode_pass("Password", salt): encode_pass(password, salt),
            encode_pass("Username", salt): encode_pass(user, salt)
        }

    with open("vault/passwords.json", "w") as out_file:
        json.dump(_json, out_file)
