#!/usr/bin/python

import sys, os

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
	comparedag.write('JOB {0} phylum.sub\n'.format(phylum))
	comparedag.write('VARS {0} ani_combo="{0}/ani_combos_{0}.txt" phylum="{0}"\n'.format(phylum))
	comparedag.write('SCRIPT PRE {0} makeANIcombos.py {0}\n'.format(phylum))
	comparedag.write('SCRIPT POST {0} combineANI.sh {0}\n'.format(phylum))

comparedag.close()