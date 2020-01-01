import json
from getpass import getpass

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

    _json[encode_pass(site, salt)] = {
        "Username": encode_pass(user, salt),
        "Password": encode_pass(password, salt)
    }

    with open("vault/passwords.json", "w") as out_file:
        json.dump(_json, out_file)