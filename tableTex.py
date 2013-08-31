#!/home/paulk/software/bin/python
from sys import argv,exit,stderr

S = {"exonic.stats":"exonic regions",
"canonical_exons.stats":"canonical transcript exons",
"probesets.stats":"probeset regions",
"exonic2.stats":"exonic regions",
"exonic.wilcox.stats":"exonic regions",
"canonical_exons.wilcox.stats":"canonical transcript exons",
"probesets.wilcox.stats":"probeset regions",
"canonical_exons.top.excl87.stats":"canonical transcript exons"
}

f = open(argv[1])
data = dict()
for row in f:
	if row[0] == '#':
		if row[1] == '#':
			thresh = row.strip()[2:-3]
		else:
			continue
	elif row[0] == '\n':
		continue
	else:
		l = row.strip().split('\t')
		if thresh not in data:
			data[thresh] = dict()
			data[thresh][l[0],l[1]] = l[2:]
		else:
			data[thresh][l[0],l[1]] = l[2:]

f.close()
#print >> stderr,data
#exit(0)

print """\
\\documentclass[10pt,a4paper]{article}
\\usepackage[latin1]{inputenc}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\usepackage{color}
\\usepackage{lscape}
\\usepackage[right=0.5in,left=0.5in]{geometry}
\\begin{document}"""

threshes = map(int,data.keys())
threshes.sort()
for t in map(str,threshes):
	print "\\begin{landscape}"
	print "\\begin{table}"
	print "\\centering"
	print "\\begin{tabular}{|"+"c|"*10 + "}"
	print "\\hline"
#	print "\multicolumn{4}{|c|}{$\\tau$ = %s; \#features = %s} \\\\"%(t,data[t]['0.1'][5])
	print "\multicolumn{10}{|c|}{top = %s; \#features = %s} \\\\"%(t,data[t]['0.1','0.1'][5])
	print "\\hline"
	if argv[2] == 't': print "$p$ [RS] & $p$ [EA] & $t$ [RS] & $t$ [EA] & A & C & B & D & OR & OR $p$-value \\\\"
	elif argv[2] == 'w': print "$p$-value & $U$-stat & OR & OR $p$-value \\\\"
	print "\\hline"
#	keys = map(float,data[t].keys())
#	keys.sort()
#	for p in map(str,keys):
	for p in data[t]:
		dp = data[t][p]
		if float(dp[7]) <= 0.05:
			#0.005	0.005	5.30666713306	5.30666713306	0	19	18	3127	3164	0.0	1.0
			print "%s&%s&%s" % (p[0],p[1],"&".join(dp[:8]+dp[10:])) +"\\\\"
#			print "%s & %.5f & \\textcolor{red}{%.5f} & \\textcolor{red}{%.5f} \\\\"%(p,float(data[t][p][0]),float(data[t][p][6]),float(data[t][p][7]))
		else:
			print "%s&%s&%s" % (p[0],p[1],"&".join(dp[:8]+dp[10:])) +"\\\\"
#			print "%s & %.5f & %.5f & %.5f \\\\"%(p,float(data[t][p][0]),float(data[t][p][6]),float(data[t][p][7]))
	print "\\hline"
	print "\\end{tabular}"
#	print "\\caption{Contingency tests for %s at normalised expression threshold of $\\tau$=%s}"%(S[argv[1]],t)
	print "\\caption{Contingency tests for %s at normalised expression threshold for top %s}"%(S[argv[1]],t)
	print "\\end{table}"
	print "\\end{landscape}"
	print
print "\\end{document}"
