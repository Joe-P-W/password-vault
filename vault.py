import os
import random

from character_map.maps import maps

def personal_salt_creation() -> str:
    return str(random.randint(100000000, 888888888))


def encode_pass(password: str, salt: str) -> str:
    salt_num = int(salt[int(salt[1])] + salt[int(salt[-1])])
    num_pass = []
    for i in range(len(password)):
        for index, value in enumerate(maps):
            if password[i] == value:
                num_pass.append(index)
                break

    salted_pass = []
    for num in num_pass:
        salted_pass.append(num-salt_num)

    hashed_pass = ""
    for index, num in enumerate(salted_pass):
        hashed_pass += maps[int(num) + index]

    return hashed_pass


def decode_pass(hashed_pass: str, salt: str) -> str:
    salt_num = int(salt[int(salt[1])] + salt[int(salt[-1])])
    salted_pass = []
    for index, value in enumerate(list(hashed_pass)):
        for i in range(len(maps)):
            if value == maps[i]:
                salted_pass.append(i-index)

    num_pass = []
    for num in salted_pass:
        num_pass.append(num+salt_num)

    password = ""
    for i in num_pass:
        for index, value in enumerate(maps):
            if i == index or i-len(maps) == index:
                password += value
                break

    return password

salt = personal_salt_creation()
encoded = encode_pass("", salt)
print(encoded)
print(decode_pass(encoded, salt))

