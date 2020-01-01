

def mask(password: str, salt: int) -> str:
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

    for i in range(1, len(letters)):
        if i * holes >= len(letters):
            break
        letters = letters[:i * holes] + letters[i * holes + 1:]

    for i in range(len(indexes)):
        if int(indexes[i]) >= len(letters):
            for x in range(1, len(letters)):
                if int(indexes[i]) >= len(letters):
                    indexes[i] = round(int(indexes[i]) / x)
        try:
            hash_.append(letters[int(indexes[i])])
        except IndexError:
            hash_.append(letters[0])

    for index, value in enumerate(list(letters)):
        if value in hash_:
            hash_.pop((index+hash_hole)%len(hash_))

    return "".join(hash_)