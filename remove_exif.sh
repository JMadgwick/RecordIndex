#!/bin/bash
images=$(ls -1v|grep .JPG)

for file in $images;
do
    convert $file -monitor -strip -quality 80 $file
done
