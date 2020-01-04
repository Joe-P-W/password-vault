import json
import os
import random

from character_map.maps import maps
from crypto_files.decode import decode_pass
from crypto_files.encode import encode_pass


def pad(length: int):
    padding = ""
    for i in range(length):
        letter = random.choice(maps)
        if letter not in ["{", "}"]:
            padding += letter

    return padding


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

    padding1 = pad(random.randint(5, 200))
    padding2 = pad(random.randint(5, 200))
    vault = padding1 + vault + padding2
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
    vault = "{" + "}".join(("{".join(vault.split("{")[1:])).split("}")[:-1]) + "}"

    with open("vault/passwords.json", "w") as vault_file:
        vault_file.write(vault)
