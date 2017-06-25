import string

SIMPLE_ENCODING = string.ascii_lowercase + ' '
BITS = 5


def char_to_bits(c):
    i = SIMPLE_ENCODING.index(c)
    b = "{0:b}".format(i)
    while len(b) < BITS:
        b = "0" + b
    return b


def encode(s):
    # s only contains lowercase alphabet letters
    return ''.join(map(char_to_bits, s))


def decode(s):
    assert len(s) % BITS == 0
    out = []
    for i in range(len(s) // BITS):
        b = s[BITS * i: BITS * (i + 1)]
        n = int(b, 2)
        assert n < len(SIMPLE_ENCODING)
        out.append(SIMPLE_ENCODING[n])
    return ''.join(out)
