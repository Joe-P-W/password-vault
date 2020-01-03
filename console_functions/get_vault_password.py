import json
import os
import sys
from getpass import getpass

from console_functions.get_salt_from_pass import get_salt_from_password
from console_functions.make_password import make_password
from crypto_files.vault_password_hasher import mask


def get_vault_password():
    if "vault_pass.json" not in os.listdir("vault"):
        make_password()
    x = 0
    while True:
        if x > 3:
            print("Too many attempts")
            sys.exit()
        else:
            vault_pass = getpass("Enter your vault password: ")
            with open("vault/vault_pass.json", "r") as in_file:
                _json = json.load(in_file)
                vault_hash = _json["hash"]
                vault_salt = _json["salt"]
            if vault_hash == mask(vault_pass, vault_salt):
                return get_salt_from_password(vault_pass)
            else:
                x += 1
                print("\nPassword incorrect try again: ")
