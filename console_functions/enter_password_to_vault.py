import json
import sys
import time
from getpass import getpass
import random

from console_functions.get_pass_from_vault import copy_to_clipboard
from console_functions.random_pass_gen import generate_password
from crypto_files.encode import encode_pass
from console_functions.get_vault_password import get_vault_password
from crypto_files.vault_handler import Vault


def enter_password_to_vault(vault: Vault):
    salt = get_vault_password()
    if salt == "go back":
        return
    site = input("What is this for? ")
    if site.lower() == "back":
        return
    user = input("Username? ")
    if user == "back":
        return
    while True:
        password = getpass("Set your password: ")
        if password.lower() == "random":
            while True:
                password = generate_password()
                check = password
                copy_to_clipboard(password)
                print("Password copied to clipboard.")
                answer = input("Did this password work y/n? ").lower()
                if answer == "y":
                    copy_to_clipboard("")
                    break
                elif answer == "back":
                    return

        elif password.lower() == "back":
            return
        else:
            check = getpass("Retype your password: ")

        if password == check:
            break
        elif check.lower() == "back":
            return
        else:
            print("\nSorry what you typed did not match try again: ")



    num = random.randint(1, 2)

    if num == 1:
        vault.vault_json[encode_pass(site, salt)] = {
            encode_pass("Username", salt): encode_pass(user, salt),
            encode_pass("Password", salt): encode_pass(password, salt)
        }

    else:
        vault.vault_json[encode_pass(site, salt)] = {
            encode_pass("Password", salt): encode_pass(password, salt),
            encode_pass("Username", salt): encode_pass(user, salt)
        }

    vault.encode_vault(salt)

    for i in range(5):
        print(f"Password entered into the vault taking you back in {5-i}.", end="\r")
        time.sleep(1)
        sys.stdout.write("\x1b[2K")
