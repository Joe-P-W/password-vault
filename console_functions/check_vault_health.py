import os

from crypto_files.encode_vault import encode_vault


def check_vault_health(salt: str):
    if "passwords.json" in os.listdir("vault"):
        message = "Please use the quit command to exit the vault as not doing this leaves off a layer of encryption"
        banner = "".join(["!" for i in message])
        print()
        print(banner)
        print(message)
        print(banner)
        print()
        encode_vault(salt)