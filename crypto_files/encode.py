from character_map.maps import maps


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
        hashed_pass += maps[(int(num) - index) % len(maps)]

    return hashed_pass



