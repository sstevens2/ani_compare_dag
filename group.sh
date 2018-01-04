#!/bin/bash

#Usage: bash group.sh spllist group

inlist=`basename $1`
group=$2

#for each line in sub inputlist run ani calculator
while read line
do
sub=`echo $line | cut -d',' -f1`
query=`echo $line | cut -d',' -f2`
./ANIcalculator -genome1fna $sub -genome2fna $query -outfile $group-$sub-$query.ani.out
done < $inlist


