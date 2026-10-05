#!/bin/bash
# Every claim in the article, in order. Needs GNU tar and Python 3.
set -e
python3 handtar.py && tar -tvf byhand.tar                      # a spec-built tar that GNU tar reads

# the checksum covers the header only
cp byhand.tar data.tar
python3 -c "b=bytearray(open('data.tar','rb').read()); b[512]=ord('X'); open('data.tar','wb').write(b)"
mkdir -p d && tar -xf data.tar -C d && echo "exit $? -> $(cat d/hello.txt)"   # exit 0, corrupted

# the 8 GiB octal limit, using a sparse file
truncate -s 9G big.bin
tar --format=ustar -cf - big.bin 2>&1 >/dev/null | head -1 || true
rm -f big.bin

# identical inputs, different archives; then the reproducible flags
mkdir -p src && for f in c a b; do echo "content of $f" > src/$f.txt; done
tar -cf one.tar -C src . ; sleep 2; touch src/*.txt; tar -cf two.tar -C src .
cmp one.tar two.tar || true
tar --sort=name --mtime='2024-01-01 00:00Z' --owner=0 --group=0 --numeric-owner \
    --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
    --format=posix -cf repro.tar -C src .

# append, and the newer copy wins
echo "version 1" > config.txt && tar -cf app.tar config.txt
echo "version 2" > config.txt && tar -rf app.tar config.txt
rm config.txt && tar -xf app.tar && cat config.txt              # version 2

# the read-cost comparison: build 2,000 files, then extract the last one each way
python3 make_many.py
python3 count_reads.py      # seekable tar vs zip
python3 count_gz.py         # tar.gz with getmember(): reads it twice for the last file
python3 count_stream.py     # tar.gz streaming, stop when found
