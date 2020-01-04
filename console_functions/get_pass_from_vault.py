import json
import subprocess
import sys
import time

from crypto_files.encode import encode_pass
from crypto_files.decode import decode_pass
from console_functions.get_vault_password import get_vault_password


def copy_to_clipboard(text):
    subprocess.run(f'{"clip" if sys.platform == "win32" else "pbcopy"}', universal_newlines=True, input=text)


def get_pass_from_vault():
    salt = get_vault_password()
    if salt == "go back":
        return
    with open("vault/passwords.json", "r") as in_file:
        keys = [decode_pass(key, salt) for key in json.load(in_file).keys()]
    while True:

        _input = input("\n\nWhat credentials do you want? ")

        if "list" in _input:
            print()
            for key in keys:
                print(key)
            print()
            continue

        if _input.lower() == "back":
            return

        if _input not in keys:
            print(f"{_input} is not listed in the password vault")

        for key in keys:
            if key == _input:
                with open("vault/passwords.json", "r") as in_file:
                    _json = json.load(in_file)

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
