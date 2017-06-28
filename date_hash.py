import hashlib
import struct
import sys

if sys.version_info >= (3,4):
    from datetime import datetime as DateTime
    from datetime import timedelta as TimeDelta
else:
    from mx.DateTime import DateTime, TimeDelta

BASE_DT = DateTime(1, 1, 1)

def date_hash(secret, username):
    # both are strings
    concat = secret + username # mind blown
    b = concat.encode('utf-8')
    m = hashlib.sha256(b)
    d = m.digest()
    i = struct.unpack('<I', d[0:4])
    t = BASE_DT + TimeDelta(minutes=i[0])
    return t.strftime('%b %d %Y %I:%M %p')

