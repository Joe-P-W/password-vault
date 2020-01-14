import json
import random

from character_map.maps import maps
from crypto_files.decode import decode_pass
from crypto_files.encode import encode_pass


class Vault:
    def __init__(self, salt):
        self.passwords = None
        self.salt = salt

    def __enter__(self):
        self.decode_vault()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.encode_vault()

    def encode_vault(self):
        vault = self.passwords

        keys = list(vault.keys())
        random.shuffle(keys)
        shuffled_vault = dict()
        for key in keys:
            shuffled_vault.update({key: vault[key]})

        vault = json.dumps(shuffled_vault)

        padding1 = self._pad(random.randint(5, 500))
        padding2 = self._pad(random.randint(5, 500))
        vault = padding1 + vault + padding2
        vault = encode_pass(vault, self.salt)

        with open("vault/passwords.txt", "w") as vault_file:
            vault_file.write(vault)

    def decode_vault(self):
        try:
            with open("vault/passwords.txt", "r") as vault_file:
                vault = vault_file.read()
        except FileNotFoundError:
            self.passwords = {}

            self.encode_vault()

            with open("vault/passwords.txt", "r") as vault_file:
                vault = vault_file.read()

        vault = decode_pass(vault, self.salt)

        vault = "}".join(("{".join(vault.split("{")[1:])).split("}")[:-1])
        vault = "{" + vault + "}"

        self.passwords = json.loads(vault)

    @staticmethod
    def _pad(length: int):
        padding = ""
        for i in range(length):
            letter = random.choice(maps)
            if letter not in ["{", "}", ":", ","]:
                padding += letter

        return padding
