# Task 1 — Cryptography

Two-stage cipher: Base64 encoding wrapped around a Beaufort cipher.

## Stage 1: Base64 decode

```bash
echo "QkFJTntiQTczX1E4Ul9BcmhIQ19YNHlHY0R9" | base64 -d
```

Result: `BAIN{bA73_Q8R_ArhHC_X4yGcD}`

This wasn't the final flag — it doesn't match the expected `BYTE{...}` format,
which was the clue that another layer of encoding was still in play.

## Stage 2: Beaufort cipher

The letters inside the braces were further encrypted with a Beaufort cipher,
key: `cybr`. Decrypted using the standard Beaufort formula
`P = (K - C) mod 26` on each letter (non-letters like digits, underscores and
braces are left untouched) — see `solve.py`.

**Final flag:** `BYTE{bY73_L8A_ChuKA_B4dLaV}`
