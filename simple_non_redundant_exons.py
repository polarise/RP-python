#!/home/paulk/software/bin/python
from __future__ import division
import random
import cPickle

f = open("/data2/paulk/RP/resources/exons.hg19.Ens66.0-based.semi_non_redundant.pic")
exons = cPickle.load(f) # somehow
f.close()

class Coordinate(object):
  def __init__(self,coord_string):
    chrom,st_sp,sd = coord_string.split(':')
    st,sp = st_sp.split('-')
    self.chrom = chrom
    self.st = int(st)
    self.sp = int(sp)
    self.sd = sd
  
  def __eq__(self,other):
    return self.st == other.st or self.sp == other.sp
   
  def __repr__(self):
    return self.chrom+":"+str(self.st)+"-"+str(self.sp)+":"+self.sd

my_dict = dict()
for e in exons: # for each exon
  coord = Coordinate(exons[e])  # create a Coordinate object
  if coord.chrom not in my_dict:  # if the chromosome has not been seen before (neither has the exon)
    my_dict[coord.chrom] = dict() # add the chromosome and put a subdictionary
    my_dict[coord.chrom][coord] = [e]   # add the coordinate and the exon list
  else: # otherwise (we have seen this chromosome before)
    count_other = 0 # set a counter on the number of times this coordinate-like is found
    for other in my_dict[coord.chrom]:  # for all coordinates under this chromosome 
      if coord == other:  # if another coordinate is equal (as defined in the Coordinate class)
        my_dict[coord.chrom][other] += [e]  # add this exon there
        count_other += 1 # increment the counter
    if not count_other: # if the counter was not incremented (no resemblance to any other coordinate in this chromosome)
      my_dict[coord.chrom][coord] = [e] # add it as a new coordinate    

non_redundant = dict()
already_taken = dict()
for chrom in my_dict: # for each chromosome
  for coord in my_dict[chrom]:  # for each Coordinate in each chromosome
    chosen = False  # assume we have not chosen yet
    while not chosen: # while we have not yet chosen a random exon
      i = random.choice(range(len(my_dict[chrom][coord])))  # get a random index for this coordinate
      rand_exon = my_dict[chrom][coord][i]  # pick the exon itself
      if not rand_exon in already_taken:   # have we taken this exon before?
        non_redundant[rand_exon] = coord.__repr__() # if not then select it 
        already_taken[rand_exon] = 0 # add it to the list of those already taken
        chosen = True # exit the while loop
        
f = open("/data2/paulk/RP/resources/exons.hg19.Ens66.0-based.non_redundant.pic",'w')
cPickle.dump(non_redundant,f,cPickle.HIGHEST_PROTOCOL)
f.close()
