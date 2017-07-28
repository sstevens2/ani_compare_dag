#!/usr/bin/python

# coding: utf-8
import glob, sys
phylum=sys.argv[1]


def makeCombos(phylum,filelist):
	with open(phylum+'/ani_combos_'+phylum+'.txt', 'w') as output:
		used=[]
		for fn1 in filelist:
			fn1 = fn1.split(phylum+'/')[1]
			for fn2 in filelist:
				fn2 = fn2.split(phylum+'/')[1]
				if fn2 in used:
					continue
				elif fn1==fn2:
					continue
				else:
					output.write(fn1+','+fn2+'\n')
			used.append(fn1)


if __name__ == "__main__":
    flist=glob.glob(phylum+'/*.fna')
    makeCombos(phylum,flist)