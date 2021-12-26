#!/bin/bash
odss=$(ls -1v|grep .ods)
IFS=$'\n'
for file in $odss;
do
    python3 requestsDiscogsSearch.py $file
done
