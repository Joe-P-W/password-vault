import json
import random
import subprocess
import sys
import os
import time

from getpass import getpass


class Vault:
    def __init__(self):
        self.__maps = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234"
                           "567890-=!\"£$%^&*()_+[];'#,./@~<>?{}:\\|\u20AC\u00A5`¬ ")
        self.__salt = self._get_vault_password()
        self.__passwords = None

    def __enter__(self):
        self.__decode_vault()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__encode_vault()

    def enter_password_to_vault(self):
        capture = self._get_vault_password()
        if capture == "go back":
            return
        site = input("What is this for? ")
        if site.lower() == "back":
            return
        user = input("Username? ")
        if user == "back":
            return
        while True:
            password = getpass("Set your password: ")
            if password.lower() == "random":
                while True:
                    password = self._generate_password()
                    check = password
                    self._copy_to_clipboard(password)
                    print("Password copied to clipboard.")
                    answer = input("Did this password work y/n? ").lower()
                    if answer == "y":
                        self._copy_to_clipboard("")
                        break
                    elif answer == "back":
                        return

            elif password.lower() == "back":
                return
            else:
                check = getpass("Retype your password: ")

            if password == check:
                break
            elif check.lower() == "back":
                return
            else:
                print("\nSorry what you typed did not match try again: ")

        num = random.randint(1, 2)

        if num == 1:
            self.__passwords[self.__encode_pass(site)] = {
                self.__encode_pass("Username"): self.__encode_pass(user),
                self.__encode_pass("Password"): self.__encode_pass(password)
            }

        else:
            self.__passwords[self.__encode_pass(site)] = {
                self.__encode_pass("Password"): self.__encode_pass(password),
                self.__encode_pass("Username"): self.__encode_pass(user)
            }

        self.__encode_vault()

        for i in range(5):
            print(f"Password entered into the vault taking you back in {5 - i}.", end="\r")
            time.sleep(1)
            sys.stdout.write("\x1b[2K")

    def get_pass_from_vault(self):
        capture = self._get_vault_password()
        if capture == "go back":
            return

        keys = [self.__decode_pass(key) for key in self.__passwords.keys()]
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
                    _json = self.__passwords

                    username = self.__decode_pass(_json[self.__encode_pass(key)][self.__encode_pass("Username")])
                    print(f'\nUsername: {username}')
                    password = self.__encode_pass("Password")
                    self._copy_to_clipboard(self.__decode_pass(_json[self.__encode_pass(key)][password]))
                    print("Password Copied to clipboard for 20 seconds")
                    for i in range(20):
                        print(f"Time left: {20 - i} ", end="\r")
                        time.sleep(1)
                        sys.stdout.write("\x1b[2K")
                    self._copy_to_clipboard("")

                    return

    def _get_vault_password(self):
        if "vault_pass.json" not in os.listdir("vault"):
            self.__make_password()
        x = 0
        while True:
            if x > 3:
                for i in range(3):
                    print(f"Vault guards coming to kick you out in {3 - i} ", end="\r")
                    time.sleep(1)
                    sys.stdout.write("\x1b[2K")
                sys.exit()
            else:
                vault_pass = getpass("Enter your vault password: ")
                if vault_pass.lower() == "back":
                    return "go back"
                with open("vault/vault_pass.json", "r") as in_file:
                    _json = json.load(in_file)
                    vault_hash = _json["hash"]
                    vault_salt = _json["salt"]
                if vault_hash == self.__mask(vault_pass, vault_salt):
                    return self._get_salt_from_password(vault_pass)
                else:
                    x += 1
                    print("\nPassword incorrect try again: ")

    def _get_salt_from_password(self, password: str) -> str:
        salt = ""
        for pass_index, letter in enumerate(list(password)):
            for index, value in enumerate(self.__maps):
                if letter == value:
                    if index % 2 == 0:
                        salt += str(index + pass_index)
                    else:
                        salt += str(index - pass_index)
        return salt

    def _pad(self, length: int) -> str:
        padding = ""
        for i in range(length):
            letter = random.choice(self.__maps)
            if letter not in ["{", "}", ":", ","]:
                padding += letter

        return padding

    def _generate_password(self) -> str:
        password = random.choice("1234567890") + random.choice("!\"£$%^&*-_=+")
        for i in range(random.randint(10, 20)):
            password += random.choice(self.__maps[:90])

        random.shuffle(list(password))

        return "".join(password)

    @staticmethod
    def _copy_to_clipboard(text):
        subprocess.run(f'{"clip" if sys.platform == "win32" else "pbcopy"}', universal_newlines=True, input=text)

    def __encode_vault(self):
        vault = self.__passwords

        keys = list(vault.keys())
        random.shuffle(keys)
        shuffled_vault = dict()
        for key in keys:
            shuffled_vault.update({key: vault[key]})

        vault = json.dumps(shuffled_vault)

        padding1 = self._pad(random.randint(5, 500))
        padding2 = self._pad(random.randint(5, 500))
        vault = padding1 + vault + padding2
        vault = self.__encode_pass(vault)

        with open("vault/passwords.txt", "w") as vault_file:
            vault_file.write(vault)

    def __decode_vault(self):
        try:
            with open("vault/passwords.txt", "r") as vault_file:
                vault = vault_file.read()
        except FileNotFoundError:
            self.__passwords = {}

            self.__encode_vault()

            with open("vault/passwords.txt", "r") as vault_file:
                vault = vault_file.read()

        vault = self.__decode_pass(vault)

        vault = "}".join(("{".join(vault.split("{")[1:])).split("}")[:-1])
        vault = "{" + vault + "}"

        self.__passwords = json.loads(vault)

    def __decode_pass(self, hashed_pass: str) -> str:
        salt_num = int(self.__salt[int(self.__salt[1])] + self.__salt[int(self.__salt[-1])])
        salted_pass = []
        for index, value in enumerate(list(hashed_pass)):
            for i in range(len(self.__maps)):
                if value == self.__maps[i]:
                    salted_pass.append((i + index) % len(self.__maps))

        num_pass = []
        for num in salted_pass:
            num_pass.append(num + salt_num)

        password = ""
        for i in num_pass:
            for index, value in enumerate(self.__maps):
                if i == index or i - len(self.__maps) == index:
                    password += value
                    break

        return password

    def __encode_pass(self, password: str) -> str:
        salt_num = int(self.__salt[int(self.__salt[1])] + self.__salt[int(self.__salt[-1])])
        num_pass = []
        for i in range(len(password)):
            for index, value in enumerate(self.__maps):
                if password[i] == value:
                    num_pass.append(index)
                    break

        salted_pass = []
        for num in num_pass:
            salted_pass.append(num - salt_num)

        hashed_pass = ""
        for index, num in enumerate(salted_pass):
            hashed_pass += self.__maps[(int(num) - index) % len(self.__maps)]

        return hashed_pass

    def __make_password(self):
        salt = random.randint(10 ** 6, 10 ** 7)
        while True:
            password = getpass("Set your password: ")
            check = getpass("Retype your password: ")
            if password == check:
                break
            else:
                print("Sorry what you typed did not match")

        with open("vault/vault_pass.json", "w") as in_file:
            _json = {
                "hash": self.__mask(password, salt),
                "salt": salt
            }
            json.dump(_json, in_file)

    @staticmethod
    def __mask(password: str, salt: int) -> str:
        letters = "1234567890-=!\"£$%^&*()_+qwertyuiop[]QWERTYUIOP{}asdfghjkl;'#ASDFGHJKL:@~\\zxcvbnm,./|ZXCVBNM<>? "
        salt = str(salt)
        holes = int(salt[0] + salt[-1])
        key = int(salt[1] + salt[-2])
        seq = int(salt[2])
        hash_hole = int(salt[3])

        indexes = []
        hash_ = []

        if seq == 1 or seq == 0:
            seq = int(str(holes)[0])

        if key == 0:
            key = int(str(holes)[-1] + str(holes)[0])

        for i in range(len(password)):
            for x in range(len(letters)):
                if password[i] == letters[x]:
                    if x == 0 or i == 0:
                        indexes.append(x + key + i)

                    elif i % x in range(0, x, seq):
                        indexes.append(x - key - i)

                    elif i % x in range(1, x, seq):
                        indexes.append(x - key + i)

                    else:
                        indexes.append(round(x * key / i))

        for i in range(len(indexes)):
            if int(indexes[i]) >= len(letters):
                for x in range(1, len(letters)):
                    if int(indexes[i]) >= len(letters):
                        indexes[i] = round(int(indexes[i]) / x)
            try:
                hash_.append(letters[int(indexes[i])])
            except IndexError:
                hash_.append(letters[0])

        _stop = False
        for index, value in enumerate(list(letters)):
            if value in hash_:
                hash_.pop((index + hash_hole) % len(hash_))
                if _stop:
                    break
                else:
                    _stop = True

        return "".join(hash_)
