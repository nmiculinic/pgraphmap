from pgraphmap.tasks import basecall, r
import argparse
import hashlib
from Bio import SeqIO
import tempfile
import os
import pysam
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("reads")
parser.add_argument("ref")
parser.add_argument("-C", action="store_true")
parser.add_argument("--batch", type=int, default=800)
parser.add_argument("sam")
args = parser.parse_args()

n = len(list(SeqIO.parse(args.reads, 'fasta')))

with open(args.reads, 'rb') as f:
    data = f.read()
    m = hashlib.sha256()
    m.update(data)
    r.set(m.hexdigest(), data)
    args.reads = m.hexdigest()

with open(args.ref, 'rb') as f:
    data = f.read()
    m = hashlib.sha256()
    m.update(data)
    r.set(m.hexdigest(), data)
    args.ref = m.hexdigest()


results = []

for i in range(0, n, args.batch):
    rest = min(n - i, args.batch)
    results.append(basecall.delay(args.reads, args.ref, args.C, i, rest))

d = tempfile.mkdtemp()
sam_files = []

for x in results:
    name = x.get()
    path = os.path.join(d, name)
    with open(path, 'wb') as f:
        f.write(r.get(name))
    sam_files.append(path)

pysam.merge('-f', args.sam, *sam_files, catch_stdout=False)
shutil.rmtree(d)
