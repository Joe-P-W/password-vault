import json
import random

from character_map.maps import maps
from crypto_files.decode import decode_pass
from crypto_files.encode import encode_pass


class Vault:
    def __index__(self):
        self.vault_json = None

    def encode_vault(self, salt: str):

        vault = self.vault_json

        keys = list(vault.keys())
        random.shuffle(keys)
        shuffled_vault = dict()
        for key in keys:
            shuffled_vault.update({key: vault[key]})

        vault = json.dumps(shuffled_vault)

        padding1 = self.pad(random.randint(5, 500))
        padding2 = self.pad(random.randint(5, 500))
        vault = padding1 + vault + padding2
        vault = encode_pass(vault, salt)

        with open("vault/passwords.txt", "w") as vault_file:
            vault_file.write(vault)

    def decode_vault(self, salt: str):
        try:
            with open("vault/passwords.txt", "r") as vault_file:
                vault = vault_file.read()
        except FileNotFoundError:
            self.vault_json = {}

            self.encode_vault(salt)

            with open("vault/passwords.txt", "r") as vault_file:
                vault = vault_file.read()

        vault = decode_pass(vault, salt)

        vault = "}".join(("{".join(vault.split("{")[1:])).split("}")[:-1])
        vault = "{" + vault + "}"

        self.vault_json = json.loads(vault)

    def pad(self, length: int):
        padding = ""
        for i in range(length):
            letter = random.choice(maps)
            if letter not in ["{", "}", ":", ","]:
                padding += letter

        return padding
