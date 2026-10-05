import io, tarfile, time, os
class Counting(io.FileIO):
    def __init__(s,*a,**k): super().__init__(*a,**k); s.read_bytes=0
    def read(s,n=-1): b=super().read(n); s.read_bytes+=len(b); return b
    def readinto(s,buf): n=super().readinto(buf); s.read_bytes+=n or 0; return n
LAST="f01999.bin"; FIRST="f00000.bin"
for target in (FIRST, LAST):
    f=Counting("many.tar.gz","rb"); t0=time.perf_counter()
    with tarfile.open(fileobj=f, mode="r:gz") as a:
        data=a.extractfile(a.getmember(target)).read()
    dt=(time.perf_counter()-t0)*1000; total=os.path.getsize("many.tar.gz")
    print(f"  {target}: read {f.read_bytes:>12,} of {total:,} compressed bytes ({100*f.read_bytes/total:5.1f}%), {dt:7.1f} ms")
