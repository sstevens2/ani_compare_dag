#!/bin/bash

while read line
do
mv $line-*.ani.out $line
tail -n 2 $line/$line-*.ani.out > $line.all.ani.out
num=`wc -l $line/ani_combos_$line.txt | cut -f1 -d' '`
cat $line.all.ani.out | sort | uniq | sed '/^\s*$/d' | head -n $num > $line.all.ani.out.cleaned
done < $1
