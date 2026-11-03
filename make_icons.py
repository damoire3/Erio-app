import zlib, struct, os
PAL = {"1": "bfe6ff", "2": "8fcff5", "a": "1f6b3a", "b": "2ea05a", "c": "6fd18a", "d": "b7e36b", "t": "4a3322", "e": "d9c9a0", "f": "b9a67a", "h": "8c7a55", "i": "1d4651", "j": "2b6470", "k": "8fe8d8", "l": "41c1b5", "m": "1f8f93", "n": "146574", "o": "e8fffb", "p": "ff9a2e", "q": "e5671b", "r": "ffc766", "E": "14101f", "s": "efe2bd", "u": "d8c694", "v": "e8b48a", "w": "e8742c", "x": "3a6fb0", "y": "6b7a3a", "z": "4a86c6", "H": "3a2a20", "W": "f6f1e7", "G": "5ed12e", "D": "2f9d1f", "I": "f1e9c8", "R": "e5231a", "O": "ff7b21", "U": "5b5bd6", "L": "3fb85a", "M": "1f7a3a", "F": "ff7fb5", "X": "e0457f", "Y": "ffd23f", "T": "5a3d2b", "Z": "7fd6d0", "Q": "d8fff6", "3": "8d8aa0", "4": "d8d5e6", "5": "a8683b", "6": "5e3b25", "7": "ff9cc4", "8": "e53935", "%": "2f6fe0", "*": "5fb3ff", "+": "e9dfc9", "=": "3b3a48"}
ICON = ["fffffhffffffffffuuTuuuuuuuuu", "ffefifffffffefffuuTujjjjjjuu", "iiiiiiiiihfhffffuuTujZZZZjuu", "iiiiiiiiiifffhffuuTujZZZZjuu", "iiiijiiiiiiifeffuuTujZZZZjuu", "ijjjjjjjiiiiffffuuTujZZZZjuu", "jjjj2jjjjiiiifffuuTujZZZZjuu", "jj22222jjjiiiiffuuTujZZZOOuu", "jHH212HHjjiiiiffuuTujZZGaauu", "2vv111vv2jjRRRifuRRRjaGaaauu", "2vv111vv2jjRERifuREaddaaZjuu", "2ww111yy2jGRRRGGGadddaaaZjuu", "2ww111yy2jGGGGGaadccaaZZZjuu", "eww111yye2GGDaaddcdaaajjjjuu", "mzzmmmyymmkGaddcccaauuuuuuuu", "mzzmmmyymkaaddccaaaaGeeeeeeu", "klkkkkQklaadcccGaaIGGGeeeus1", "QQQQmQQkaadccOGaaaIGGGseeue1", "mmmmmmmmadccOdaaIIGGGUueeee1", "QQQQmQQQdcccdaaaGGGGUUeeeee1", "kkFkQkQaddddaaGGGGGUUOOeeee1", "QFXFQQQaadaaaQQQQQQQOOOeeee1", "FFFFFkkkaaaakkkkLkkkkklkeee1", "QFYFQkkkaaaLLLLLLLLLLLLLkkkk", "QLFLLLLLLLLLLLLLLLLkkkkkkkkk", "LLLLLLLLLLLLLLLLLLLLLLkkkkkk", "lLLLLLMMMMMMMMMMMMMMMMMMMMML", "kllLlkllMMMMMMMMMMMMMMMMMnnm"]
SCENE = ["21111bbbbcbbbbcccccccccccbb111bbbcbbbbacccccccbb", "111bcccacccccccbcccccccccbbb1cccccccccbbccccccab", "11bcccccccccbbbccccccccccbbbbbbbbcbbbbbbbacccccc", "11cccccccccccbbbbbbcbbbbbabb1bbbbbbdbbbbcccccccb", "1bbacbccccccccbdbbbbbcbbbbb111bbbbdbbbbcccccccbb", "21bbcbcccccccccbabbbbbbbab11112111bbbbbbbcbbdcbb", "bcdbbbbbbcbbbbbbbcb1b111111111111111bbbbbbcbccdb", "dccccbbbbbdbdbabbbbb1111111111111111ZZbbbdbbcccb", "bbbbbbbbbbcccdcbcccbb111111111111111ZZZZZ1bbcccb", "bbbbbbbbtbbbbbabbbbbbb11111111111111ZZZZZ11ccccc", "bbbbbbbbchbbbbbbbbbbbhhhhhhhhhhhhhhhhhThhhbbcccb", "bbbbbbbbtT1bbbbbcbbb1T11T11T11T11T11T1TT11Tbcccb", "bbbbbbbbhhhhhhhahhhhhhhhhhhhhhhhhFhhhhThhhhbFccb", "bbbbbbdbeTeeTeeTeeTeeTeeTeeTeeTeeTeFTeTTeeTbbcbb", "bbbbbcbeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeTeeeeebbbb", "eebbeceeeeeeeeeeeeeeeeeeeeeeeeeeeeeeuuTuuuuubbbb", "eebeeceeeeeeeeeeeeeeeeeeeeeeeeeeeeeeuuTuuuuuuubu", "eebfhcffffffffffhffffffffhffffffffffuuTuuuuuuuuu", "11bfefefffhffffffeffffefifffffffefffuuTujjjjjjuu", "11bhffffeffffehfffffiiiiiiiiihfhffffuuTujZZZZjuu", "111fffeffffffffffffiiiiiiiiiiifffhffuuTujZZZZjuu", "111fffffffffefhefiiiiiiijiiiiiiifeffuuTujZZZZjuu", "111ffffffffffefffiiiijjjjjjjiiiiffffuuTujZZZZjuu", "11cbfffffhheffffiiiijjjj2jjjjiiiifffuuTujZZZZjuu", "cccccbffffeffffiiiijjj22222jjjiiiiffuuTujZZZOOuu", "ccRcccbffhfefefiiiijjHH212HHjjiiiiffuuTujZZGaauu", "cccccbbbcbffhfiiiijj2vv111vv2jjRRRifuRRRjaGaaauu", "bbcbRbcccccbheiiiijj2vv111vv2jjRERifuREaddaaZjuu", "fbbbbcccRcccbeiiiijj2ww111yy2jGRRRGGGadddaaaZjuu", "ehfbfbcccccbcbiiiijj2ww111yy2jGGGGGaadccaaZZZjuu", "fffhffbbcbcRcccbijj2eww111yye2GGDaaddcdaaajjjjuu", "ehhffffbbbbbcbbkmmmmmzzmmmyymmkGaddcccaauuuuuuuu", "ffffhfefebfbbbkkkmmmmzzmmmyymkaaddccaaaaGeeeeeeu", "fffffeffhfffkkkkkkkkklkkkkQklaadcccGaaIGGGeeeus1", "fffeefffhfkkkkkkkkQQQQQQmQQkaadccOGaaaIGGGseeue1", "fffheffffkkkkkkkkkkmmmmmmmmmadccOdaaIIGGGUueeee1", "ffffefekkkkkQQQQQQQQQQQQmQQQdcccdaaaGGGGUUeeeee1", "fhffefklkkkkkkkkkkkkkkFkQkQaddddaaGGGGGUUOOeeee1", "ffhfkkkkQQQQQQQQQQQQQFXFQQQaadaaaQQQQQQQOOOeeee1", "eekkkkkkQkQkkQkkkkkkFFFFFkkkaaaakkkkLkkkkklkeee1", "QkkkQkkkQkkkQlkkQkkkQFYFQkkkaaaLLLLLLLLLLLLLkkkk", "QkQQQkQQQkQQQkQQQkQQQLFLLLLLLLLLLLLLLLLkkkkkkkkk", "mnnmnnmnnlllllollolkLLLLLLLLLLLLLLLLLLLLLLkkkkkk", "nnmqnmkoolklllllollklLLLLLMMMMMMMMMMMMMMMMMMMMML", "nmnnmnnmnkkkkllkllllkllLlkllMMMMMMMMMMMMMMMMMnnm", "ppppEnknokklllkkkkllollllllllklllollLlllnnmnnmnn", "ppppppnnmklkkkkkqkkllllllllokkklllllklllmnnmnnmn", "rrrrrnnmnmkkkkkqqqkmmokmmmmmmkmkkmmkkkkonmnnmnnm", "mnnmnnqnnkmkkkmpmkmmmmmmmmmmmmmkkkmmkmmmnnonnmnn", "nnmnnmqqkkkmpppppppmmmmmmmmmmkmmkmkkkkkmlnnmnnmn", "nmnnmnqqqkmpppppppEpmmmmmmmmkkkkkkkkkmmmnmnnmnnm", "mnnmnnqqqkppprrrrrpppmmmlmmmkkkkkkkkmkmmnnmnnmnn", "nnmnnmqqmmmrrrrrrrrrmmklmmkmmomkmmkmmmmmmnnmnnmn", "nmnnmnqmnmkkprrrrrpkmkkkmkkkmmomkmmkmkkmnmknmnnm", "mnnmnnmnnmkkkmmpkkkkkmkkmmkmmmmkmkkkkkkknnmnnmnn", "nnmnnmkqmnoknnnknnnknnnnnnnnknnnqnnknkknmnnmnnmn", "nmnnmnqqqnnonnnnnnnnnnnknnnnnnnqqqnnnknnnmnnmnnm", "mnnmnnmnkpnnnnnnnqknnnqnnnnnnnnpnnnnnnnnnnmnnmnn", "nnmnnmpppppppnnnqqnnnkqqnnnnpppppppnnnnnmnnmnnmn", "nmnnmpEpppppppnqqqnnnnqqqnnpppppppEpnnnnnmnnmnnm", "mnnmppprrrrrpppqqqnknnqqqkppprrrrrpppnnnnnmnnmnn", "nnmnnrrrrrrrrrnnqqknonqqnnnrrrrrrrrrnnnlmnnmnnmn", "nmnnmnprrrrrpnnnnqnnnnqnnknnprrrrrpnnnnnnmnnmnnm", "mnnmnnmnnpnnnnnnnnnnnnnnnnnnnnnpnnnnnnnnnnmnnmnn"]
COL = {k: (int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16), 255) for k, v in PAL.items()}
DARK = (0x0c, 0x09, 0x16, 255)
NONE = (0, 0, 0, 0)

def png(path, W, art, unit, bg):
    solid = not art
    art = art or ['.']
    h, w = len(art), len(art[0])
    ox, oy = (W - w * unit) // 2, (W - h * unit) // 2
    raw = bytearray()
    cache = {}
    def row(k):
        o = bytearray(bytes(bg) * ox)
        for ch in art[k]:
            o += bytes(COL.get(ch, bg)) * unit
        o += bytes(bg) * (W - ox - w * unit)
        return b'\x00' + bytes(o)
    for y in range(W):
        k = (y - oy) // unit if not solid and oy <= y < oy + h * unit else -1
        if k not in cache:
            cache[k] = row(k) if k >= 0 else b'\x00' + bytes(bg) * W
        raw += cache[k]
    def ch(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'wb').write(b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', W, W, 8, 6, 0, 0, 0)) + ch(b'IDAT', zlib.compress(bytes(raw), 9)) + ch(b'IEND', b''))

png('assets/icon-only.png', 1024, ICON, 36, DARK)
png('assets/icon-foreground.png', 1024, ICON, 24, NONE)
png('assets/icon-background.png', 1024, None, 1, DARK)
png('assets/splash.png', 2732, SCENE, 14, DARK)
png('assets/splash-dark.png', 2732, SCENE, 14, DARK)
print('icones ok')
