#!/bin/bash

images=$(ls -1v|grep 220621)
newname=""
match="(.*)_[^.]*(\..*)"

declare -i side=1
# Only works when text extracted, 6 total 'sides' (2 text files + JPG)
# Do not run with just JPG, though files will not be overwritten (mv -nv)
declare -i number=40

for file in $images;
do
    if [ $side -lt 4 ]; then
        [[ $file =~ $match ]]
        newname=R${BASH_REMATCH[1]}_$number-A${BASH_REMATCH[2]}
        mv -nv $file $newname
        echo "$newname $side"
        side=$(($side+1))
    else
        [[ $file =~ $match ]]
        newname=R${BASH_REMATCH[1]}_$number-B${BASH_REMATCH[2]}
        mv -nv $file $newname
        echo "$newname $side"
        if [ $side = 6 ]; then
            number=$(($number+1))
            side=1
        else
            side=$(($side+1))
        fi
    fi
done
