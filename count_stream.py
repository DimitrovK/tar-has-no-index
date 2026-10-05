import io, tarfile, time, os
class Counting(io.FileIO):
    def __init__(s,*a,**k): super().__init__(*a,**k); s.read_bytes=0
    def read(s,n=-1): b=super().read(n); s.read_bytes+=len(b); return b
    def readinto(s,buf): n=super().readinto(buf); s.read_bytes+=n or 0; return n
total=os.path.getsize("many.tar.gz")
for target in ("f00000.bin","f01999.bin"):
    f=Counting("many.tar.gz","rb"); t0=time.perf_counter()
    with tarfile.open(fileobj=f, mode="r|gz") as a:      # '|' = pure stream, no seeking at all
        for m in a:
            if m.name==target:
                data=a.extractfile(m).read(); break
    dt=(time.perf_counter()-t0)*1000
    print(f"  stream {target}: read {f.read_bytes:>12,} bytes ({100*f.read_bytes/total:5.1f}%), {dt:7.1f} ms")
