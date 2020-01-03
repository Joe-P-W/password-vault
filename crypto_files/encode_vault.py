import json
import os
import random

from crypto_files.decode import decode_pass
from crypto_files.encode import encode_pass


def encode_vault(salt: str):
    with open("vault/passwords.json", "r") as vault_file:
        vault = json.load(vault_file)

    keys = list(vault.keys())
    random.shuffle(keys)
    shuffled_vault = dict()
    for key in keys:
        shuffled_vault.update({key: vault[key]})

    with open("vault/passwords.json", "w") as vault_file:
        json.dump(shuffled_vault, vault_file)

    with open("vault/passwords.json", "r") as vault_file:
        vault = vault_file.read()

    vault = encode_pass(vault, salt)

    with open("vault/passwords.txt", "w") as vault_file:
        vault_file.write(vault)

    os.remove("vault/passwords.json")


def decode_vault(salt: str):
    try:
        with open("vault/passwords.txt", "r") as vault_file:
            vault = vault_file.read()
    except FileNotFoundError:
        vault = {}
        with open("vault/passwords.json", "w") as vault_file:
            json.dump(vault, vault_file)

        encode_vault(salt)

        with open("vault/passwords.txt", "r") as vault_file:
            vault = vault_file.read()

    vault = decode_pass(vault, salt)

    with open("vault/passwords.json", "w") as vault_file:
        vault_file.write(vault)
