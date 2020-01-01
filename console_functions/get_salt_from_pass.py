from character_map.maps import maps


def get_salt_from_password(password: str) -> str:
    salt = ""
    for pass_index, letter in enumerate(list(password)):
        for index, value in enumerate(maps):
            if letter == value:
                if index % 2 == 0:
                    salt += str(index + pass_index)
                else:
                    salt += str(index - pass_index)
    return salt
