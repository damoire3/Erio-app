import zlib, struct, os
ART = ['................', '.........gg..gg.', '.........ggGGgg.', '......y...gGGg..', '...........GG...', '..........pppp..', '..........PPPP..', '...y......PPPP..', '......ppppPPPP..', '......PPPPPPPP..', '......PPPPPPPP..', '..ppppPPPPPPPP..', '..PPPPPPPPPPPP..', '..PPPPPPPPPPPP..', '..PPPPPPPPPPPP..', '................']
COL = {'g': (0x8f, 0xe3, 0xb0, 255), 'G': (0x34, 0xb3, 0x6a, 255), 'p': (0xb9, 0xa2, 0xff, 255), 'P': (0x7c, 0x5c, 0xf0, 255), 'y': (0xf5, 0xe2, 0x7a, 255)}
DARK = (0x0c, 0x09, 0x16, 255)
NONE = (0, 0, 0, 0)

def write(path, w, h, rowfn):
    raw = bytearray()
    cache = {}
    for y in range(h):
        k = rowfn(y)
        if k not in cache:
            cache[k] = b'\x00' + cache_row(k, w)
        raw += cache[k]
    def chunk(t, d):
        c = struct.pack('>I', len(d)) + t + d
        return c + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b'')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'wb').write(png)

def art_image(path, w, unit, bg):
    ox = (w - 16 * unit) // 2
    def row(k):
        out = bytearray(bytes(bg) * ox)
        for ch in ART[k]:
            out += bytes(COL[ch] if ch != '.' else bg) * unit
        out += bytes(bg) * (w - ox - 16 * unit)
        return bytes(out)
    global cache_row
    cache_row = lambda k, w_: bg_row(bg, w_) if k < 0 else row(k)
    write(path, w, w, lambda y: (y - ox) // unit if ox <= y < ox + 16 * unit else -1)

def bg_row(bg, w): return bytes(bg) * w

art_image('assets/icon-only.png', 1024, 56, DARK)
art_image('assets/icon-foreground.png', 1024, 40, NONE)
art_image('assets/icon-background.png', 1024, 0 or 1, DARK) if False else None
# fond uni
def solid(path, w, bg):
    global cache_row
    cache_row = lambda k, w_: bg_row(bg, w_)
    write(path, w, w, lambda y: 0)
solid('assets/icon-background.png', 1024, DARK)
art_image('assets/splash.png', 2732, 24, DARK)
art_image('assets/splash-dark.png', 2732, 24, DARK)
print('icons ok')
