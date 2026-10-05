"""Build the 2,000-file test archives used by the count_*.py scripts."""
import os, tarfile, zipfile, gzip, shutil
N, SZ = 2000, 50_000
os.makedirs("many", exist_ok=True)
blob = os.urandom(SZ)
for i in range(N):
    with open(f"many/f{i:05d}.bin", "wb") as f: f.write(blob)
names = sorted(os.listdir("many"))
with tarfile.open("many.tar", "w", format=tarfile.PAX_FORMAT) as t:
    for n in names: t.add(f"many/{n}", arcname=n)
with zipfile.ZipFile("many.zip", "w", compression=zipfile.ZIP_STORED) as z:
    for n in names: z.write(f"many/{n}", arcname=n)
with open("many.tar", "rb") as src, gzip.open("many.tar.gz", "wb", compresslevel=1) as dst:
    shutil.copyfileobj(src, dst)
for f in ("many.tar", "many.zip", "many.tar.gz"):
    print(f"  {f}: {os.path.getsize(f):,} bytes")
