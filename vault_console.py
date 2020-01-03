import sys

from console_functions.check_vault_health import check_vault_health
from console_functions.enter_password_to_vault import enter_password_to_vault
from console_functions.get_pass_from_vault import get_pass_from_vault
from console_functions.get_vault_password import get_vault_password
from crypto_files.encode_vault import encode_vault, decode_vault

salt = get_vault_password()
check_vault_health(salt)
decode_vault(salt)

while True:
    command = input("command? ")

    if command == "quit":
        encode_vault(salt)
        sys.exit()

    elif command == "enter password" or command == "enter pass":
        enter_password_to_vault()

    elif command == "get password" or command == "get pass":
        get_pass_from_vault()
