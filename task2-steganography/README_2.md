# Task 2 — Steganography

A PNG file (`challenge.png`) that was deliberately corrupted at the file-format
level, with the flag hidden as text inside the image itself.

## 1. Diagnosing the corruption

PNG files are made of length-prefixed "chunks" (IHDR, IDAT, IEND, etc.), each
with its own CRC checksum. Walking the file chunk-by-chunk and verifying each
CRC showed:

- The `IHDR` chunk's CRC was invalid (the header data itself was fine — just
  the checksum had been tampered with).
- An `IDAT` chunk's declared `length` field didn't match its real length,
  which throws off every chunk boundary calculated after it (since the next
  chunk's position depends on the previous chunk's declared length).

## 2. Finding the real chunk boundaries

Since declared lengths couldn't be trusted, I searched the raw bytes for the
literal chunk-type tags (`IHDR`, `IDAT`, `IEND`) to find where chunks
*actually* started. The gaps between consecutive marker positions gave the
true length of each chunk. I rebuilt the file using these true boundaries,
recomputing the correct length and CRC32 for every chunk.

## 3. Decompressing the pixel data

PNG pixel data is zlib-compressed. The standard decompressor refuses to
output anything if the trailing Adler-32 checksum doesn't match — so I
stripped the 2-byte zlib header and decompressed as **raw DEFLATE**
(`zlib.decompressobj(-15)`), which bypasses that checksum entirely.

## 4. Finding the hidden splice

For an RGB image, the expected decompressed size is
`height * (1 + width*3)` (the `+1` per row is PNG's per-scanline filter-type
byte, which must be 0–4). The actual decompressed stream was **108,710 bytes
larger** than expected.

Walking row by row and checking each scanline's filter-type byte found the
exact point where the stream stopped making sense (row 323) — meaning
108,710 bytes of unrelated data had been spliced into the middle of the
real pixel stream at that point.

## 5. Removing the splice and rendering

Cutting that inserted block out and reassembling the stream restored it to
the correct expected size. Reversing PNG's per-row filtering (Sub/Up/
Average/Paeth) on the result and rendering it as an RGB image revealed a
photo with a line of readable text on a black bar near the bottom —
hidden "in plain sight" directly in the image content, not as a separate
embedded file.

## Tools used
Python 3, `struct`, `zlib` (standard library only), Pillow for rendering.

See `solve.py` for the full repair + extraction script.

**Final flag:** `flag{g0t 1t in plAin sight}`
