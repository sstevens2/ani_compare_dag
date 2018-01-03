#!/bin/bash

while read dirname
do
mkdir $dirname/errs
done < groupslist.txt
