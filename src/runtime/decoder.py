KEY = 23


def decode(data):
    return "".join(chr(b ^ KEY) for b in data)
