#!/usr/bin/python

# coding: utf-8
import glob, sys

""" makeANIcombos.py : script to make file with every possible combination of genomes (comma separated)
	if only one argument is given (group(directory/phylum) name) then it will run all v all within
	that directory
	to run a specific group vs another  group (eg. one lake vs the other lake)
		also give a file for each set (max 3) with each genome on each line 
			- this will also get around if files don't end in '.fna'
"""


def usage():
	print('If you want to make all combos in a directory the usage is (only works on ".fna" files)')
	print('makeANIcombos.py group/phylum/directory_name(no "/" at end)')
	print('             OR')
	print('if you want to make all combos between two lists in a group/phylum/directory')
	print('makeANIcombos.py group/phylum/directory_name firstlist secondlist')
	print('for this 2nd option lists must contain the group directory name in path')

def makeCombos(group, filelist, filelist2):
	with open(group+'/ani_combos_'+group+'.txt', 'w') as output:
		used=[]
		for fn1 in filelist:
			if fn1.contains('/'):
				fn1 = fn1.split(group+'/')[1]
			for fn2 in filelist2:
				if fn2.contains('/'):
					fn2 = fn2.split(group+'/')[1]
				if fn2 in used:
					continue
				elif fn1 == fn2:
					continue
				else:
					output.write(fn1+','+fn2+'\n')
			used.append(fn1)


if __name__ == "__main__":
	if len(sys.argv) == 1: 	# quick check for at least one argument
		usage()
		exit(2)
	elif len(sys.argv) == 2: # no lists given, will run all v all for all files ending in .fna in group/directory
		group=sys.argv[1]
		flist = glob.glob(group+'/*.fna')
		flist2 = glob.glob(group+'/*.fna')
	elif len(sys.argv) == 4:
		group=sys.argv[1]
		flist = [line.rstrip('\n') for line in open(sys.argv[2],'r')]
		flist2 = [line.rstrip('\n') for line in open(sys.argv[3],'r')]
	else:
		usage()
		exit(2)
	makeCombos(group, flist, flist2)

