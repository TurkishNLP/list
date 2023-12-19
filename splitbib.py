#!/usr/bin/env python3
import sys, os, re
from pybtex.database import parse_file
import codecs
import latexcodec
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('input_file')
ap.add_argument('--output-dir', '-O', default="bibfiles")
ap.add_argument('--output-file', '-o')
args = ap.parse_args()

if args.output_file:
    outfp = open(args.output_file, "w")
else:
    outfp = sys.stdout

db = parse_file(args.input_file)

for key, entry in db.entries.items():
    bibfile = os.path.join(args.output_dir, (key + '.bib'))
    print(bibfile)
    with open(bibfile, 'wt') as f:
        print(entry.to_string('bibtex'), file=f)
