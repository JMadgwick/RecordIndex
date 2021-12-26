#!/bin/bash
if [[ -z "${GOOGLE_APPLICATION_CREDENTIALS}" ]]; then
    echo 'Not in virtualenv or GOOGLE_APPLICATION_CREDENTIALS not set'
    exit 1
fi
echo "Enter Folder Name:"
read foldername
cd $foldername

images=$(ls -1v|grep .jpg)
for file in $images;
do
    python ../extractText.py $file
done
