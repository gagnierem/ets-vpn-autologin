import base64
import hmac
import struct
import time
import hashlib

def get_totp(secret_b32: str, digits: int = 6, period: int = 30, algo=hashlib.sha1):
    # 1. Base32 decode (since secret is normal uppercase string)
    secret_bytes = base64.b32decode(secret_b32, casefold=True)

    # 2. Time counter
    counter = int(time.time() // period)
    msg = struct.pack(">Q", counter)

    # 3. HMAC with decoded secret
    h = hmac.new(secret_bytes, msg, algo).digest()

    # 4. Dynamic truncation
    offset = h[-1] & 0x0F
    code = (struct.unpack(">I", h[offset:offset+4])[0] & 0x7fffffff) % (10 ** digits)

    return str(code).zfill(digits)


# # Example usage:
# secret = "YXFTKG2VCRJMPJRJ"   # replace with your uppercase secret
# print("TOTP:", get_totp(secret))
