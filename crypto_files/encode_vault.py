import os

from crypto_files.decode import decode_pass
from crypto_files.encode import encode_pass


def encode_vault(salt: str):
    with open("vault/passwords.json", "r") as vault_file:

        vault = vault_file.read()

    vault = encode_pass(vault, salt)

    with open("vault/passwords.txt", "w") as vault_file:
        vault_file.write(vault)

    os.remove("vault/passwords.json")


def decode_vault(salt: str):
    with open("vault/passwords.txt", "r") as vault_file:
        vault = vault_file.read()

    vault = decode_pass(vault, salt)

    with open("vault/passwords.json", "w") as vault_file:
        vault_file.write(vault)
