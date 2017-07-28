#!/usr/bin/python

import sys, os, makeANIcombos

"""Writes the external DAG file and all the submission files for each phylum in phylum list given.
	Must be one level up ani_combos_phylumname.txt for each phylum
"""

__author__ = "Sarah Stevens"
__email__ = "sstevens2@wisc.edu"


def usage():
	print "Usage: writeCompareDAG.py phylumdirs.txt"


if len(sys.argv) != 2:
	usage()
	exit()


with open(sys.argv[1],'r') as f:
	phydirs=f.readlines()

## writing out the config options for the compare dag
with open('compare.dag.config','w') as configout:
	configout.write('DAGMAN_MAX_JOBS_SUBMITTED = 1000\n')
	configout.write('DAGMAN_MAX_JOBS_IDLE = 100\n')
	configout.write('DAGMAN_MAX_POST_SCRIPTS = 4\n')
	configout.write('DAGMAN_MAX_PRE_SCRIPTS = 4\n')

comparedag = open('compare.dag', 'w') 

for phylum in phydirs: # Makes 2 lines for each
	#write phylum and postscript job to DAG
	phylum=phylum.rstrip('\n')
	makeANIcombos.makeCombos(phylum)
	comparedag.write('SPLICE {0} {0}.spl')
	with open('{0}/ani_combos_{0}.txt'.format(phylum),'r') as combos:
		combolist=combos.readlines()
	with open(phylum+'.spl', 'w') as splice:
		for i, combo in ennumerate(combolist):
			combo=combo.rstrip('\n')
			sub,query=combo.split(',')
			splice.write('JOB {0}{1} phylum.sub\n'.format(combo,i))
			splice.write('VARS {0}{1} phylum="{0}" sub="{2}" query="{3}"\n'.format(phylum,i,sub,query))

comparedag.close()






