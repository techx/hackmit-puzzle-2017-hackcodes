import hashlib
import math
from builtins import bytes


def hack_hash(message, charset, length):
    """
    Hash used across Hack puzzles for secure but stateless
    info transfer.

    Args:
        message (str): the message to hash
        charset (:obj:`list` of :obj:`str`): a list of the possible elements
        length (int): the desired number of elements to concatenate in hash

    Returns:
        str: Concatenated length-long list consisting of charsets.
    """
    digests = []
    i = 0
    bits_for_charset = int(math.ceil(math.log2(len(charset))))
    bytes_for_charset = int(math.ceil(bits_for_charset/8))
    while len(digests) * 64 < length * bytes_for_charset:
        digests.append(hashlib.sha512(
            bytes(str(i) + message, 'utf-8')).digest())
        i += 1
    digest = bytes(b'').join(digests)
    out = []
    for i in range(length):
        b = digest[i*bytes_for_charset:(i+1)*bytes_for_charset]
        n = int.from_bytes(b, byteorder='little', signed=False)
        out.append(charset[n % len(charset)])
    return ''.join(out)
