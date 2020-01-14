import json
import subprocess
import sys
import time

from crypto_files.encode import encode_pass
from crypto_files.decode import decode_pass
from console_functions.get_vault_password import get_vault_password
from crypto_files.vault_handler import Vault


def copy_to_clipboard(text):
    subprocess.run(f'{"clip" if sys.platform == "win32" else "pbcopy"}', universal_newlines=True, input=text)


def get_pass_from_vault(vault: Vault):
    salt = get_vault_password()
    if salt == "go back":
        return

    keys = [decode_pass(key, salt) for key in vault.vault_json.keys()]
    while True:

        _input = input("\n\nWhat credentials do you want? ")

        if "list" in _input:
            print()
            for key in sorted(keys):
                print(key)
            print()
            continue

        if _input.lower() == "back":
            return

        if _input not in keys:
            print(f"{_input} is not listed in the password vault")

        for key in keys:
            if key == _input:
                _json = vault.vault_json

                username = decode_pass(_json[encode_pass(key, salt)][encode_pass("Username", salt)], salt)
                print(f'\nUsername: {username}')
                password = encode_pass("Password", salt)
                copy_to_clipboard(decode_pass(_json[encode_pass(key, salt)][password], salt))
                print("Password Copied to clipboard for 20 seconds")
                for i in range(20):
                    print(f"Time left: {20-i} ", end="\r")
                    time.sleep(1)
                    sys.stdout.write("\x1b[2K")
                copy_to_clipboard("")

                return
