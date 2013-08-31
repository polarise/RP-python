#!/home/paulk/software/bin/python
import sys
from key_functions import n_ary_sum,motif_generator

N1 = 2222222
N2 = 2222222
base = 3

"""
digits = max(len(str(N1)),len(str(N2)))

N1_list = map(int,list(str(N1).zfill(digits)))
N2_list = map(int,list(str(N2).zfill(digits)))


#print N1_list,N2_list

try:
	assert len(N1_list) == len(N2_list)
except:
	raise ValueError("Input digits of unequal length")
	sys.exit(1)
	
if base in N1_list or base in N2_list:
	raise ValueError("Base digit cannot appear in numbers")
	sys.exit(1)

carry = [0] * (digits + 1)
result = [0] * (digits + 1)

indices = range(digits)[::-1]

for i in indices:
	result[i + 1] = (N1_list[i] + N2_list[i] + carry[i + 1]) % base
	carry[i] = (N1_list[i] + N2_list[i] + carry[i + 1]) // base
result[0] = carry[0]
"""

result = n_ary_sum(N1,1,7,base)[1:]
print N1
print 1
print result

result = 0
for i in xrange(27):
	result = n_ary_sum(result,001,3,3)[1:]
	print result

alpha = ['A','C','G','T']
size = 6
instances = motif_generator(alpha,size)
instances.sort()
print instances

from cPickle import dump,HIGHEST_PROTOCOL
f = open("hexamers.pic",'w')
dump(instances,f,HIGHEST_PROTOCOL)
f.close()

#instances_modified = [i[:2]+"-"+i[2:] for i in instances]
#print instances_modified
print
print len(instances),"motifs for you"
sys.exit(1)

print "base %s" % base
print " " + "".join(map(str,N1_list)).zfill(digits)
print "+" + "".join(map(str,N2_list)).zfill(digits)
print "".join(map(str,carry)).zfill(digits + 1)
print "-" * (digits + 1)
print "".join(map(str,result)).zfill(digits + 1)
print "-" * (digits + 1)
