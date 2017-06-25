import hashlib
from builtins import bytes
import struct


def hack_hash(message, charset, length):
    """
    Return a 64-character string that is the hash of message.

    given a unicode message and charset list
    """
    digests = []
    i = 0
    while len(digests) * 64 < length:
        digests.append(hashlib.sha512(
            bytes(str(i) + message, 'utf-8')).digest())
        i += 1
    digest = bytes(b'').join(digests)
    return ''.join([charset[int(b) % len(charset)] for b in digest])[:length]
