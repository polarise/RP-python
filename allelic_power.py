from __future__ import division
from scipy import *
from scipy import stats
import pylab

p_o = 0.5
q_o = 1 - p_o
z_alpha = 1.96

As = [1,1.25,2,5,10,100]
legend_val = ""

for A in As:
	p_a = A/(A + 1)
	q_a = 1 - p_a
	betas = []
	ns = xrange(1,500,1)
	for n in ns:
		z_beta = (p_o + z_alpha*sqrt(p_o*q_o/n) - p_a)/sqrt(p_a*q_a/n)
		betas.append(stats.norm.sf(z_beta)*100)

	pylab.figure(1)
	pylab.plot(ns,betas)
	legend_val += "A = %s, "%A
	pylab.ylim((-5,105))

print legend_val[:-2]
pylab.legend(legend_val[:-2].split(","))
pylab.title("Power (1-$\\beta$) to detect ASE against number of reads",fontsize=14,weight='bold')
pylab.xlabel("Number of reads",fontsize=13,weight='roman')
pylab.ylabel("Power to detect (1-$\\beta)\\times 100$%",fontsize=13,weight='roman')
pylab.grid()
pylab.savefig( "fig3.eps", dpi=300, format="eps" )
