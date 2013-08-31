#!/home/paulk/software/bin/python
from __future__ import division
from sys import argv,exit,stderr
import rpy2.robjects as R

cor = R.r['cor']
qunif = R.r['qunif']
runif = R.r['runif']
sort = R.r['sort']
plot = R.r['qqplot']
hist = R.r['hist']
lines = R.r['lines']
pdf = R.r['pdf']
par = R.r['par']
dev_off = R.r['dev.off']
roundR = R.r['round']
log = R.r['log']
pi = R.r['pi']
abline = R.r['abline']
expression = R.r['expression']


def sampleNosToLabels(nums):
	res = list()
	vals = {'3':'C1','4':'T1','5':'T2','6':'C2','7':'C3','8':'T3','9':'T4','10':'C4'}
	for n in nums:
		res += [vals[n]]
	return ",".join(res)

try:
	prefix = argv[1]
except IndexError:
	print >> stderr,"Usage: %s [core|all|difference]" % argv[0]
	exit(1)

#assert prefix == 'core' or prefix == 'all'

# uncomment if doing Q-Q plots
if prefix == 'core': quniform = log(sort(qunif(runif(123266)))); s = slice(13,29,1); quniform = -quniform.ro
elif prefix == 'all': quniform = log(sort(qunif(runif(131997)))); s = slice(12,28,1); quniform = -quniform.ro
elif prefix == 'difference': s = slice(28,44,1)
elif prefix == 'full_difference': s = slice(33,49,1)

#f = open("permutation_tests/%s_norm_ps_pi0.unique" % prefix)
f = open("permutation_tests/%s_sanitised.paired_pi0.unique" % prefix)
files = [row.strip().split('\t') for row in f]
f.close()

import fnmatch
import os

#png("qqplots_%s.png" % prefix,width=2400,height=3600,res=300,units="px",pointsize=13)
pdf("plots/qqplots_%s.pdf" % prefix,width=7,height=10)
par(mfrow=R.IntVector([4,2]))

#png("qqplots_groups.png",width=2400,height=2400,res=300,units="px",pointsize=15)
c = 0
for myfile,rho in files:
	if c >= 1: break
	f = open("permutation_tests/"+myfile)
	data = list()
	data = [row.strip().split('\t')[3] for row in f]
	data.sort()
	#data = log(R.FloatVector(map(float,data)))
	data = R.FloatVector(map(float,data))
	#data = -data.ro
	f.close()
	#print file+"\t"+str(cor(data,quniform,method="pearson")[0])
	samples = myfile[s].split('_')
#	print samples
#	exit(0)
	main = "(%s) vs. (%s)\npi_0 = %s" % (sampleNosToLabels(samples[:4]),sampleNosToLabels(samples[4:]),roundR(float(rho),digits=4)[0])
#	plot(quniform,data,col="red",main=main,xlab="uniform quantiles",ylab="p-value quantiles",ylim=R.IntVector([0,12]),pch=20,cex=0.5)
	hist(data,main=main,xlab="pvalues",ylab="density",cex=1.2,freq=False)
	#abline(0,1,col="#888888ff",lty=2)
	abline(h=1,col="#f80c3e",lty=2,lwd=2)
	abline(h=float(rho),col="#0b12a9",lty=2,lwd=2)
	c += 0
dev_off()
