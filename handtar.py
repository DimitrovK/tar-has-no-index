import struct

def header(name, size, mtime=0, mode=0o644, uid=0, gid=0, typeflag=b"0",
           uname=b"", gname=b""):
    # POSIX ustar: fixed 512-byte header, numeric fields are OCTAL ASCII
    h = bytearray(512)
    def put(off, length, val):
        h[off:off+len(val)] = val[:length]
    put(0, 100, name.encode())                      # name
    put(100, 8, b"%07o\0" % mode)                   # mode
    put(108, 8, b"%07o\0" % uid)                    # uid
    put(116, 8, b"%07o\0" % gid)                    # gid
    put(124, 12, b"%011o\0" % size)                 # size, 11 octal digits
    put(136, 12, b"%011o\0" % mtime)                # mtime
    put(148, 8, b" " * 8)                           # checksum field = spaces while computing
    h[156:157] = typeflag                           # type: '0' = regular file
    put(257, 6, b"ustar\0")                         # magic
    put(263, 2, b"00")                              # version
    put(265, 32, uname)
    put(297, 32, gname)
    chksum = sum(h) & 0o777777                      # simple sum of all 512 bytes
    put(148, 8, b"%06o\0 " % chksum)                # then written back as octal
    return bytes(h)

def add(name, data):
    pad = (-len(data)) % 512
    return header(name, len(data)) + data + b"\x00" * pad

out  = add("hello.txt", b"first file\n")
out += add("world.txt", b"second file\n")
out += b"\x00" * 1024                               # two zero blocks terminate the archive
open("byhand.tar", "wb").write(out)
print(f"  wrote byhand.tar, {len(out)} bytes = {len(out)//512} blocks of 512")
