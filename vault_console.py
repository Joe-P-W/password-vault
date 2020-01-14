import sys
import os
import traceback
from datetime import datetime
from console_functions.enter_password_to_vault import enter_password_to_vault
from console_functions.get_pass_from_vault import get_pass_from_vault
from console_functions.get_vault_password import get_vault_password
from crypto_files.vault_handler import Vault


def main(vault: Vault):

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        command = input("<command?> ")

        if command == "quit" or command == "exit":
            break

        elif command == "enter password" or command == "enter pass":
            enter_password_to_vault(vault)

        elif command == "get password" or command == "get pass":
            get_pass_from_vault(vault)




if __name__ == "__main__":

    vault = Vault()

    try:
        os.system("title Vault Doors")
        salt = get_vault_password()
        os.system("title Vault Doors")
        vault.decode_vault(salt)
        main(vault)
    except (SystemExit, KeyboardInterrupt):
        pass
    except:
        error = traceback.format_exc()
        with open(f"error_logger/error_{datetime.now().strftime('%d-%m-%Y_%H-%M')}.txt", "w") as error_file:
            error_file.write(error)
        raise
    finally:
        try:
            vault.encode_vault(salt)
        except NameError:
            pass
