from pgraphmap.tasks import basecall, r
import argparse
import hashlib
from Bio import SeqIO
import tempfile
import os
import pysam
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("reads", help="Query file we wish to align (FASTA/FASTQ)")
parser.add_argument("ref", help="Reference sequence FASTA")
parser.add_argument("-C", action="store_true", help="Whether the reference is circular")
parser.add_argument("--batch", type=int, default=800, help="Number of reads for each worker task")
parser.add_argument("sam", help="Output sam file to write results to")
args = parser.parse_args()

ext = os.path.splitext(args.reads)[1]
if ext in [".fa", ".fasta"]:
    n = len(list(SeqIO.parse(args.reads, 'fasta')))
elif ext in [".fastq"]:
    n = len(list(SeqIO.parse(args.reads, 'fastq')))
else:
    raise ValueError("Unknown read extension " + ext)


with open(args.reads, 'rb') as f:
    data = f.read()
    m = hashlib.sha256()
    m.update(data)
    args.reads = m.hexdigest() + os.path.splitext(args.reads)[1]
    r.set(args.reads, data)

with open(args.ref, 'rb') as f:
    data = f.read()
    m = hashlib.sha256()
    m.update(data)
    args.ref = m.hexdigest() + os.path.splitext(args.ref)[1]
    r.set(args.ref, data)


results = []

for i in range(0, n, args.batch):
    rest = min(n - i, args.batch)
    results.append(basecall.delay(args.reads, args.ref, args.C, i, rest))

d = tempfile.mkdtemp()
os.makedirs(d, exist_ok=True)

sam_files = []

for x in results:
    name = x.get()
    path = os.path.join(d, name)
    with open(path, 'wb') as f:
        f.write(r.get(name))
    sam_files.append(path)

pysam.merge('-f', args.sam, *sam_files, catch_stdout=False)
shutil.rmtree(d)
