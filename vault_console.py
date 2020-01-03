import sys

from console_functions.enter_password_to_vault import enter_password_to_vault
from console_functions.get_pass_from_vault import get_pass_from_vault
from console_functions.get_vault_password import get_vault_password
from console_functions.make_password import make_password
from crypto_files.encode_vault import encode_vault, decode_vault

salt = get_vault_password()
decode_vault(salt)

while True:
    command = input("command? ")

    if command == "quit":
        encode_vault(salt)
        sys.exit()
#make_password()
#enter_password_to_vault()
#get_pass_from_vault()
