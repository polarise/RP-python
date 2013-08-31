#!/home/paulk/software/bin/python
from sys import argv,exit,stderr

try:
	fn = argv[1]
	choice = argv[2]
	ofn = argv[3]
except IndexError:
	print >> stderr,"Enter gene file."
	print >> stderr,"Usage:./createGTF.py <gene_file> <1|2> <outfile>"
	print >> stderr,"1 - GTF around genes"
	print >> stderr,"2 - GTF around exons"
	print >> stderr,"3 - full GTF"
	exit(1)

f = open(fn,'r')
g = open(ofn,'w')
for line in f:
	# use the following line if you want to use genes as they are
	if choice == '1':
		g_id,gname,chrom,st,sp,sd = line.strip().split('\t')
		print >> g,"chr%s\tSelected_genes\tgene\t%s\t%s\t.\t%s\t.\tgene_id \"%s\"; transcript_id \"%s\"; gene_name \"%s\";" % (chrom,st,sp,sd,g_id,g_id,gname)
	# use the following line if you want to use exons uniquely
	elif choice == '2':
		g_id,exno,chrom,st,sp,sd,txs = line.strip().split('\t')
		print >> g,"chr%s\tSelected_genes\tgene_exon\t%s\t%s\t.\t%s\t.\tgene_id \"%s_%s\"; transcript_id \"%s_%s\";" % (chrom,st,sp,sd,g_id,exno,g_id,exno)
	elif choice == '3':
		g_id,exno,chrom,st,sp,sd,txs = line.strip().split('\t')
		print >> g,"chr%s\tSelected_genes\tfull_exon\t%s\t%s\t.\t%s\t.\tgene_id \"%s\"; transcript_id \"%s\"; exon_number \"%s\";" % (chrom,st,sp,sd,g_id,txs,exno)
	else:
		print >> stderr,"You have entered an invalid choice. Only enter 1 (normal) or 2 (by exons only)."
f.close()
g.close()
