#!/home/paulk/software/bin/python

path = "/home/paulk/RP/output2/%sC/Genic/genes.fpkm_tracking"

data = dict()
for s in xrange(3,11):
	f = open(path%s)
	for line in f:
		if line[0] == 't': continue
		l = line.strip().split('\t')
		if l[0] not in data:
			data[l[0]] = {s:[float(l[9])]}
		else:
			if s not in data[l[0]]:
				data[l[0]][s] = [float(l[9])]
			else:
				data[l[0]][s] += [float(l[9])]
	f.close()

g = open("genic.expr",'w')
for d in data:
	print >> g,d+"\t"+"\t".join(map(str,[max(data[d][s]) for s in xrange(3,11)]))
g.close()

"""
path = "/home/paulk/RP/output2/%sC/Exonic/genes.fpkm_tracking"

data = dict()
for s in xrange(3,11):
        f = open(path%s)
        for line in f:
                if line[0] == 't': continue
                l = line.strip().split('\t')
                if l[0] not in data:
                        data[l[0]] = [l[9]]
                else:
                        data[l[0]] += [l[9]]
        f.close()

g = open("exonic.expr",'w')
for d in data:
        print >> g,":".join(d.split('_'))+"\t"+"\t".join(data[d])
g.close()


"""

