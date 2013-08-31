#!/home/paulk/software/bin/python
from sys import argv

print """\
\\documentclass[10pt,a4paper]{article}
\\usepackage[latin1]{inputenc}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\usepackage{color}
\\usepackage[right=0.5in,left=0.5in]{geometry}
\\begin{document}"""
f = open(argv[1])
data = dict()
new_block = True
for row in f:
	if row[0] == '#':
		if row[1] == '#':
			top = row.strip()[2:-3]
		else:
			continue
	else:
		if row[0] == '\n':
			print "\\hline"
			print "\\end{tabular}\\\\"
			print "\\footnotemark[1]{$p$-value cutoff used for RNA-Seq (RS)}\\\\"
			print "\\footnotemark[2]{$p$-value cutoff used for exon array (EA)}\\\\"
			print "\\footnotemark[3]{\#significant (S) from RS}\\\\"
			print "\\footnotemark[4]{\#significant from EA}\\\\"
			print "\\footnotemark[5]{\#not-significant (N) from RS}"
			print "\\end{table}"
			print
			new_block = True
		else:
			l = row.strip().split('\t')
			if new_block:
				print "\\begin{table}"
				print "\\centering"
				print "\\begin{tabular}{|"+"c|"*(len(l)-1)+"}"
				print "\\hline"
				print "\\multicolumn{10}{|c|}{top %s features; \#features = %s} \\\\" % (top,l[8])
				print "\\hline"
				print "$p$[RS]\\footnotemark[1] & $p$[EA]\\footnotemark[2] & $t$[RS] & $t$[EA] & $S_{RS}\\footnotemark[3]S_{EA}\\footnotemark[4]$ & $N_{RS}\\footnotemark[5]S_{EA}$ & $S_{RS}N_{EA}$ & $N_{RS}N_{EA}$ & OR & $p$[OR] \\\\"
				print "\\hline"
				new_block = False
			if float(l[10]) <= 0.05: print "\\textcolor{red}{%.3f} & \\textcolor{red}{%.3f} & \\textcolor{red}{%.5f} & \\textcolor{red}{%.5f} & \\textcolor{red}{%.0f} & \\textcolor{red}{%.0f} & \\textcolor{red}{%.0f} & \\textcolor{red}{%.0f} & \\textcolor{red}{%.5f} & \\textcolor{red}{%.5f} \\\\" % tuple(map(float,l[:8]+l[9:]))
			else: print "%.3f & %.3f & %.5f & %.5f & %.0f & %.0f & %.0f & %.0f & %.5f & %.5f \\\\" % tuple(map(float,l[:8]+l[9:]))
print "\\end{document}"
f.close()

