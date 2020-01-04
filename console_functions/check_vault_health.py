import os

from crypto_files.encode_vault import encode_vault


def check_vault_health(salt: str):
    if "passwords.json" in os.listdir("vault"):
        encode_vault(salt)
        return "false"

    return "true"
