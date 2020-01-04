import sys
import os
from console_functions.enter_password_to_vault import enter_password_to_vault
from console_functions.get_pass_from_vault import get_pass_from_vault


def main():
    while True:
        command = input("<command?> ")

        if command == "quit" or command == "exit":
            sys.exit()

        elif command == "enter password" or command == "enter pass":
            enter_password_to_vault()

        elif command == "get password" or command == "get pass":
            get_pass_from_vault()

        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    os.system("title Vault")
    if sys.argv[1] == "false":
        message = "Please use the quit/exit command to exit the vault as not" \
                  " doing this leaves off a layer of encryption"
        banner = "".join(["!" for i in message])
        print()
        print(banner)
        print(message)
        print(banner)
        print()

    main()

