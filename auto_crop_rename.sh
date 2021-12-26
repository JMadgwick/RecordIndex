#!/bin/bash
cd Original

images=$(ls -1v|grep .JPG)
filename=""

declare -i side=1
declare -i number=1

for file in $images;
do
    if [ $side = 1 ]; then
        filename=`date +%d%m%y-%H%M`_$number-A
        convert $file -monitor -crop 2994x2994+1623+305 -strip -deskew 40% -quality 80 ../$filename.jpg
        side=$(($side+1))
    else
        filename=`date +%d%m%y-%H%M`_$number-B
        convert $file -monitor -crop 2994x2994+1623+305 -strip -deskew 40% -quality 80 ../$filename.jpg
        side=1
        number=$(($number+1))
    fi
done
