"""
Task 1 - Cryptography
Two-stage cipher: Base64 -> Beaufort cipher
"""
import base64

ciphertext = "QkFJTntiQTczX1E4Ul9BcmhIQ19YNHlHY0R9"

# Stage 1: Base64 decode
stage1 = base64.b64decode(ciphertext).decode()
print("After Base64 decode:", stage1)
# -> BAIN{bA73_Q8R_ArhHC_X4yGcD}
# Note: this doesn't match the expected BYTE{...} format, which signals
# another layer of encoding is still in play.

# Stage 2: Beaufort cipher decrypt
# Beaufort decryption formula: P = (K - C) mod 26
# (the same formula is used for both encrypting and decrypting in Beaufort,
# since it's a reciprocal/self-inverse cipher)
def beaufort(text, key):
    result = []
    key = key.upper()
    ki = 0
    for ch in text:
        if ch.isalpha():
            c = ord(ch.upper()) - ord('A')
            k = ord(key[ki % len(key)]) - ord('A')
            p = (k - c) % 26
            out = chr(p + ord('A'))
            result.append(out if ch.isupper() else out.lower())
            ki += 1
        else:
            result.append(ch)  # leave digits, braces, underscores untouched
    return ''.join(result)

KEY = "cybr"
flag = beaufort(stage1, KEY)
print("Final flag:", flag)
# -> BYTE{bY73_L8A_ChuKA_B4dLaV}
