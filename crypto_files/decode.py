from character_map.maps import maps


def decode_pass(hashed_pass: str, salt: str) -> str:
    salt_num = int(salt[int(salt[1])] + salt[int(salt[-1])])
    salted_pass = []
    for index, value in enumerate(list(hashed_pass)):
        for i in range(len(maps)):
            if value == maps[i]:
                salted_pass.append((i+index) % len(maps))

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
