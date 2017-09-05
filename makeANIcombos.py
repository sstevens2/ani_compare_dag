#!/usr/bin/python

# coding: utf-8
import glob, sys

""" makeANIcombos.py : script to make file with every possible combination of genomes (comma separated)
	if only one argument is given (phylum/directory name) then it will run all v all within
	that directory
	to run a specific set vs a specific set (eg. one lake vs the other lake)
		also give a file for each set (max 3) with each genome on each line 
			- this will also get around if files don't end in '.fna'
"""


def usage():
	print('If you want to make all combos in a directory the usage is (only works on ".fna" files)')
	print('makeANIcombos.py phylum/directory_name(no "/" at end)')
	print('             OR')
	print('if you want to make all combos between two lists in a phylum/directory')
	print('makeANIcombos.py phylum/directory_name firstlist secondlist')
	print('for this 2nd option lists must contain the phylum directory name in path')

def makeCombos(phylum, filelist, filelist2):
	with open(phylum+'/ani_combos_'+phylum+'.txt', 'w') as output:
		used=[]
		for fn1 in filelist:
			fn1 = fn1.split(phylum+'/')[1]
			for fn2 in filelist2:
				fn2 = fn2.split(phylum+'/')[1]
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
	elif len(sys.argv) == 2: # no lists given, will run all v all for all files ending in .fna in phylum/directory
		phylum=sys.argv[1]
		flist = glob.glob(phylum+'/*.fna')
		flist2 = glob.glob(phylum+'/*.fna')
	elif len(sys.argv) == 4:
		phylum=sys.argv[1]
		flist = [line.rstrip('\n') for line in open(sys.argv[2],'r')]
		flist2 = [line.rstrip('\n') for line in open(sys.argv[3],'r')]
	else:
		usage()
		exit(2)
	makeCombos(phylum, flist, flist2)

