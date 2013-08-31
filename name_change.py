#!/home/paulk/software/bin/python
from sys import argv,stderr,stdout
import argparse

parser = argparse.ArgumentParser(description="Script to replace a column in a file with another identifier given a map between identifiers.")
parser.add_argument('infile',help="the file whose column is to be swapped")
parser.add_argument('-m','--map',help="the map of current to required identifiers")
parser.add_argument('-c','--column',type=int,default=0,help="the 0-based index of the column to be swapped")
parser.add_argument('-o','--outfile',help="outfile; optional [default: stdout]")

args = parser.parse_args()

mapfile = args.map
colno = args.column
infile = args.infile
outfile = args.outfile

names = dict()
f = open(mapfile)
for row in f:
	l = row.strip().split('\t')
	names[l[0]] = l[1]
f.close()

count = 0
f = open(infile)
if outfile: g = open(outfile,'w')
else: g = stdout
for row in f:
	l = row.strip().split('\t')
	try:
#		print names[l[0]]+"\t"+"\t".join(l[1:])
		print >> g,"\t".join(l[:colno]+[names[l[colno]]]+l[colno+1:])
	except KeyError:
		count += 1
f.close()
if outfile: g.close()
print >> stderr,"missing %s" % count
