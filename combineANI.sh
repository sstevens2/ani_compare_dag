#!/bin/bash

while read line
do
mkdir $line/anioutput/
while read combo;
do 
sub=`echo $combo | cut -d',' -f1`
query=`echo $combo | cut -d',' -f2`
output=$line-$sub-$query.ani.out
mv $output $line/anioutput
done < $line/ani_combos_$line.txt
tail -n 2 $line/anioutput/*.ani.out > $line.all.ani.out
num=`wc -l $line/ani_combos_$line.txt | cut -f1 -d' '`
cat $line.all.ani.out | sort | uniq | sed '/^\s*$/d' | head -n $num > $line.all.ani.out.cleaned
done < $1
