#!/bin/bash

while read dirname
do
mkdir $dirname/errs
done < phyladirs.txt
