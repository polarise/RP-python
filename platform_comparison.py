#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
#from scipy import *
#from scipy import stats
from cPickle import load
from key_functions import *
import argparse

parser = argparse.ArgumentParser(description="Script to perform normalisation then statistical testing")
parser.add_argument('-p','--feature',help="file containing the feature expression estimates")
parser.add_argument('-m','--meta-feature',help="file containing the metafeature expression estimates")
parser.add_argument('-o','--outfile',help="output file (required)")
parser.add_argument('type',choices='ep',help="'e' - exonic; 'p' - probeset")
parser.add_argument('-t','--test',choices='tw',default='t',help="the statistical test to carry out: t - t-test; w - wilcoxon test")
parser.add_argument('-v','--var-equal',default=False,action='store_true',help="the equality of variance assumption [default: not equal]")
parser.add_argument('-k','--kind',default='difference',help="the kind of normalisation to perform; either 'difference' (default) or 'quotient'")
parser.add_argument('-n','--normalised-data',help="file for data already normalised")
parser.add_argument('-s','--samples',nargs='+',type=int,default=[4,5,8,9,3,6,7,10],help="samples in order cases-controls e.g. 4 5 8 9 3 6 7 10")
parser.add_argument('-M','--metaprobesets-grouped',default="/home/paulk/RP/resources/metaprobesets_grouped.pic",help="the map from metaprobeset to probeset [default: /home/paulk/RP/resources/metaprobesets_grouped.pic]")

args = parser.parse_args()

ps_file = args.feature
mps_file = args.meta_feature
outfile = args.outfile
test = args.test
var_equal = args.var_equal
t = args.type
k = args.kind
nfn = args.normalised_data
cascon = args.samples
mps_dic = args.metaprobesets_grouped

if test == 't':
	test_type = "unpaired t-test"
elif test == 'w':
	test_type = "unpaired wilcoxon"

header_line = ['p','t','S',' ','#','\t','C','Y','a']

print >> stderr,"#Reading in feature data..."
if not isinstance(nfn,str):
	ps_data = dict()
	f = open(ps_file)
	for row in f:
		if row[0] in header_line: continue
		l = row.strip().split('\t')
		if t == 'e':
			ps_data[l[0]] = map(float,l[1:]) # uncomment for rna-seq
		elif t == 'p':
			ps_data[int(l[0])] = map(float,l[1:])
	f.close()

	mps_data = dict()
	f = open(mps_file)
	for row in f:
		if row[0] in header_line: continue
		l = row.strip().split('\t')
		if t == 'e':
			mps_data[l[0]] = map(float,l[1:])	# uncomment for rna-seq
		elif t == 'p':
			mps_data[int(l[0])] = map(float,l[1:])
	f.close()

	if t == 'p':
		print >> stderr,"Warning: using %s as the metaprobeset to probeset map. Ensure you change it as required." % mps_dic
		f = open(mps_dic)
		mps2ps = load(f)
		f.close()

		# reverse the above map
		ps2mps = dict()
		for m in mps2ps:
			for p in mps2ps[m]:
				ps2mps[p] = m

	# normalisation
	if t == 'p': normalised_data,missing_lg = normalise(ps_data,mps_data,ps2mps,k)
	elif t == 'e': normalised_data,missing_lg = normalise_rnaseq(ps_data,mps_data)
	
else: # the data is already normalised
	normalised_data = dict()
	f = open(nfn)
	for row in f:
		l = row.strip().split('\t')
		if t == 'p':
			normalised_data[l[0],l[1]] = list()
			for i in xrange(2,len(l)):
				try:
					normalised_data[l[0],l[1]] += [float(l[i])]
				except ValueError:
					normalised_data[l[0],l[1]] += ['NA']
		elif t == 'e':
			normalised_data[l[0]] = list()
			for i in xrange(1,len(l)):
				try:
					normalised_data[l[0]] += [float(l[i])]
				except ValueError:
					normalised_data[l[0]] += ['NA']
	f.close()
	missing_lg = []

# make the normalised data file
print >> stderr,"#Writing normalised data to file..."
if not isinstance(nfn,str): dict_to_file(normalised_data,outfile+".normalised",t)

# stat test 
print >> stderr,"#Performing statistical tests..."
test_results = statistical_test(normalised_data,cascon,test_type,var_equal)

print >> stderr,"#Writing tests file..."
dict_to_file(test_results,outfile+".tests",t)

print >> stderr,"#%s metaprobesets missing."%len(missing_lg)
