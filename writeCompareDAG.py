#!/usr/bin/python

import sys, os, makeANIcombos, glob

"""Writes the external DAG file and all the submission files for each group in group list given.
	Must be one level up ani_combos_groupname.txt for each group
"""

__author__ = "Sarah Stevens"
__email__ = "sstevens2@wisc.edu"


def usage():
	print "Usage: writeCompareDAG.py groupslist.txt splitsize(int)"


if len(sys.argv) != 3:
	usage()
	exit()

with open(sys.argv[1],'r') as f:
	groupdirs=f.readlines()
splitsize=int(sys.argv[2])

## writing out the config options for the compare dag
with open('compare.dag.config','w') as configout:
	configout.write('DAGMAN_MAX_JOBS_SUBMITTED = 1000\n')
	configout.write('DAGMAN_MAX_JOBS_IDLE = 100\n')
	configout.write('DAGMAN_MAX_POST_SCRIPTS = 4\n')
	configout.write('DAGMAN_MAX_PRE_SCRIPTS = 4\n')

comparedag = open('compare.dag', 'w') 

for group in groupdirs: # Makes 2 lines for each
	#write group and postscript job to DAG
	group = group.rstrip('\n')
	# check if there are 2 file lists to matchup for combos (must end in 'genome_list.txt')
	glist = glob.glob(group+'/*genome_list.txt')
	if len(glist) == 2:
		flistname, flist2name = glist
		flist = [line.rstrip('\n') for line in open(flistname,'r')]
		flist2 = [line.rstrip('\n') for line in open(flist2name,'r')]
	elif len(glist) == 0:
		flist = glob.glob(group+'/*.fna')
		flist2 = glob.glob(group+'/*.fna')
	else:
		print('STRANGE NUMBER OF genome_lists.txt files found in {0}.  Fix setup!'.format(group))
		exit(1)
	makeANIcombos.makeCombos(group, flist, flist2)
	comparedag.write('SPLICE {0} {0}.spl\n'.format(group))
	with open('{0}/ani_combos_{0}.txt'.format(group),'r') as combos:
		combolist=combos.readlines()
	os.system('split -a 5 -d -l {1} {0}/ani_combos_{0}.txt spllists/ani_combos_{0}.txt.'.format(group,splitsize))
	splits = glob.glob('spllists/ani_combos_{0}.txt.*'.format(group))
	with open(group+'.spl', 'w') as splice:
		start=1
		for split, splitlist in enumerate(splits):
			splice.write('JOB {0}{1} group.sub\n'.format(group,split))
			subcombolist = [line.rstrip('\n') for line in open(splitlist)]
			splitsubcombolist=[x.split(',') for x in subcombolist]
			subcombolist=[j for i in splitsubcombolist for j in i] #better subcombolist
			subcombolistpath=[group+"/"+x for x in subcombolist]
			transferlist=','.join(set(subcombolistpath))
			splice.write('VARS {0}{1} group="{0}" spllist="{2}" totransfer="{3}"\n'.format(group,split,splitlist,transferlist))

comparedag.close()






