#!/bin/bash

tail -n 2 $1/$1-*.ani.out > $1.all.ani.out
num=`wc -l $1/ani_combos_$1.txt | cut -f1 -d' '`
cat $1.all.ani.out | sort | uniq | sed '/^\s*$/d' | head -n $num > $1.all.ani.out.cleaned
