import io, tarfile, zipfile, sys, time

class Counting(io.FileIO):
    """A real file that tallies every byte the parser asks for, and every seek."""
    def __init__(self, *a, **k):
        super().__init__(*a, **k); self.read_bytes = 0; self.seeks = 0
    def read(self, n=-1):
        b = super().read(n); self.read_bytes += len(b); return b
    def readinto(self, buf):
        n = super().readinto(buf); self.read_bytes += n or 0; return n
    def seek(self, *a):
        self.seeks += 1; return super().seek(*a)

LAST = "f01999.bin"
for kind in ("tar","zip"):
    f = Counting(f"many.{kind}", "rb")
    t0 = time.perf_counter()
    if kind == "tar":
        with tarfile.open(fileobj=f, mode="r:") as a:
            data = a.extractfile(a.getmember(LAST)).read()
    else:
        with zipfile.ZipFile(f) as a:
            data = a.read(LAST)
    dt = (time.perf_counter()-t0)*1000
    total = __import__("os").path.getsize(f"many.{kind}")
    print(f"  {kind}: read {f.read_bytes:>12,} of {total:,} bytes "
          f"({100*f.read_bytes/total:5.1f}%), {f.seeks:>5} seeks, {dt:7.1f} ms, got {len(data):,} bytes")
