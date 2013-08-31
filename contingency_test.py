#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
import rpy2.robjects as R
from scipy import stats
import argparse
options = R.r['options']
options(warn=-1)

fisher_test = R.r['fisher.test']
matrix = R.r['matrix']
Rlist = R.r['list']
U1 = {0.0143:0,0.0286:1,0.0571:2,0.1:3,0.1714:4,0.2429:5}
U2 = {0.0143:0,0.0286:1,0.0571:2,0.1:3,0.1714:4,0.2429:5}

parser = argparse.ArgumentParser(description="Script to perform a contingency test on two vectors of data.")
parser.add_argument('infile',help="file formated as identifier,columns of Var1 and Var2")
parser.add_argument('-p','--thresh',type=float,nargs=2,help="threshold of p-value about which to count first for Var1 then Var2 e.g. 0.05 0.01")
parser.add_argument('-o','--outfile',help="output file to write significant-significant exons (optional)")
parser.add_argument('-t','--test',choices='tw',default='t',help="the statistical test to carry out: t - t-test; w - wilcoxon test")

args = parser.parse_args()

fn = args.infile
p1,p2 = args.thresh
assert 0 <= p1 <= 1 and 0 <= p2 <= 1
test = args.test
if test == 'w':
	assert p == 0.0143 or p == 0.0286 or p == 0.0571 or p == 0.1 or p == 0.1714 or p == 0.2429
ofn = args.outfile

"""
Creates a contingency table of the following form:
						Var2
						Cond1		Cond2
Var1	Cond1	A				B
			Cond2	C				D
			
from data that has two columns at threshold t. i.e. A = #{Var1i && Var2i | Var1i <= t && Var2i <= t} and so on...
"""

data = dict()
f= open(fn)
for row in f:
	l = row.strip().split('\t')
	data[l[0]] = map(float,l[1:])
f.close()

if test == 't':
	# get the t-statistic from the p-value assuming a two equal-sample unpaired test
	t1 = abs(stats.t.interval(1-p1,4.281)[0])
	t2 = abs(stats.t.interval(1-p2,4.281)[0])
	A = [w for w in data if abs(data[w][0]) >= t1 and abs(data[w][1]) >= t2]
	B = [w for w in data if abs(data[w][0]) >= t1 and abs(data[w][1]) < t2]
	C = [w for w in data if abs(data[w][0]) < t1 and abs(data[w][1]) >= t2]
	D = [w for w in data if abs(data[w][0]) < t1 and abs(data[w][1]) < t2]
elif test == 'w':
	# get the U-statistic from the table
	t1 = U1[p1]
	t2 = U2[p2]
	A = [w for w in data if (data[w][0] <= t1 or 16-data[w][0] <= t1) and (data[w][1] <= t2 or 16-data[w][1] <= t2)]
	B = [w for w in data if (data[w][0] <= t1 or 16-data[w][0] <= t1)and (data[w][1] > t2 or 16-data[w][1] > t2)]
	C = [w for w in data if (data[w][0] > t1 or 16-data[w][0] > t1)and (data[w][1] <= t2 or 16-data[w][1] <= t2)]
	D = [w for w in data if (data[w][0] > t1 or 16-data[w][0] > t1) and (data[w][1] > t2 or 16-data[w][1] > t2)]	
	

d = matrix(R.IntVector([len(A),len(C),len(B),len(D)]),nrow=2)
result = fisher_test(d)

if test == 't': print >> stderr,"\t".join(map(str,[p1,p2,t1,t2,len(A),len(C),len(B),len(D),len(A)+len(B)+len(C)+len(D),result[2][0],result[0][0]]))
elif test == 'w': print >> stderr,"\t".join(map(str,[p1,p2,t1,t2,len(A),len(C),len(B),len(D),len(A)+len(B)+len(C)+len(D),result[2][0],result[0][0]]))

if ofn:
	f = open(ofn,'w')
	for q in A:
		if (data[q][0] >= t1 and data[q][1] >= t2) or (data[q][0] <= -t1 and data[q][1] <= -t2):
			print >> f,"\t".join([q]+map(str,data[q]))
	f.close()
