#!/bin/bash

while read dirname
do
if [ ! -d $dirname/errs ]; then
mkdir $dirname/errs
fi
if [ ! spllists/ ]; then
mkdir spllists/
fi
done < groupslist.txt
