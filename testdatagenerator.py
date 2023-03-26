import random
import string


def integers(filename: str, size: int, intrange: (int, int) = (0,100), sep: str = ","):
    result = ""
    for _ in range(size):
        result += str(random.randint(intrange[0], intrange[1])) + sep
    result = result.removesuffix(sep)
    with open(filename, "w") as file:
        file.write(result)


integers("testdata5.txt", 10)

def strings(filename: str, size: int, length_per_string: int = 3, sep: str = ","):
    chars = list(string.digits + string.ascii_uppercase)
    result = ""
    for _ in range(size):
        for _ in range(length_per_string):
            result += chars[random.randint(0, 35)]
        result += sep
    result = result.removesuffix(sep)
    with open(filename, "w") as file:
        file.write(result)

#strings("test_string_data1.txt", 128, 5)