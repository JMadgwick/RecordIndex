Record Indexing helper scripts
==============================

This repo contains some scripts written to automate the indexing of a
large collection of records. Specifically 78 RPM shellac records. The
process for doing this was approximately:

1.  Photograph each side of every record in a predetermined set (e.g.
    records from the same label).
2.  Place these photos into a folder for that set (e.g. 'Set\_1'). Then
    move them into a subdirectory named 'Original'.
3.  Run the `auto_crop_rename.sh` script in the set directory.
4.  Run the `automatedExtract.sh` script (from the parent directory) to
    extract text for all the records in that set.
5.  Run the `processText.py` program to collate the details for all the
    records in the set into a single tsv file.
6.  Manually edit the tsv file to correct any mistakes with the label
    and catalogue number columns and save this as an ODS.
7.  Repeat above steps for all record sets.
8.  Run the `automatedDiscogs.sh` script to create a new ODS sheet for
    each set with additional information from and links to Discogs.
9.  Run `mergeDiscogs.py` to merge together all the Discogs ODS files.
    This creates one sheet with all details together.

These scripts are provided only because they might be useful to someone
else. They are incomplete in many ways and are not 'production ready' - 
e.g. error handling is not implemented for the most part.

What each script does
---------------------

### rename\_fix.sh

Sometimes when taking photos a mistake might happen - such as taking two
photos of one side or missing a side. In this case the naming sequence
will get out of sync. Fixing this manually can be a lot of work
depending on how many files need to be renamed. This script automated
the process; it doesn't take any arguments and needs to be edited
depending on the renaming to be done.

### remove\_exif.sh

Removes EXIF metadata from all JPG files in the current directly and
reduce the quality to 80. It uses the `convert` utility from ImageMagick
for this. This is useful when uploading images as not all websites
automatically remove EXIF details.

### auto\_crop\_rename.sh

Takes all files in the 'Original' directory, crops them to zoom in on
the centre label and saves them to a new file in the current directory.
The new file has a filename of the current datetime plus a sequence
number and the record side (A/B).

### automatedExtract.sh

Takes a directory name as input and runs the `extractText.py` Google
Cloud Vision text extraction program on every jpg file in the directory.
It also checks the required environment variable is set before doing
this.

### automatedDiscogs.sh

Runs the `requestsDiscogsSearch.py` ODS Discogs program on every ODS
file in the directory. The only special bit in the script is setting the
'IFS' environment variable to consider only newlines (and not spaces)
when iterating through the output of 'ls'.

### extractText.py

Using Google Cloud Vision, this takes a filename of an image in the
current directory, sends it to Google, takes the recognised text
response and puts it into into two text files. One contains the
recognised text and the likely language, the other contains each word
plus its location (x,y) in the image.

### processText.py

Takes a directory name as input, gets all the records and adds their
details to a tsv file (tabbed separated sheet). These details include
the filename, text extracted from side A/B, links to the images for both
sides and a guess for the label and catalogue number (based on numbers
appearing on both A & B sides).

### processRussianText.py

Does the same as `processText.py` but is designed for Russian records.
The primary difference is Google Cloud translation is used to create an
English translation of the detected Russian text. This is then added as
an extra column.

### requestsDiscogsSearch.py

Takes an existing ODS file containing processed (and manually corrected)
record information. It then sends a request to the Discogs API to search
for the record (using the label and catalogue number). If there is a
match on Discogs, links to the pages(s) on Discogs are added along with
the title for the first hit. This enhanced ODS file is saved with an
identical name but with 'Discogs' appended.

### mergeDiscogs.py

The purpose of this script is to merge together multiple ODS files
created by the `requestsDiscogsSearch.py` program into a single ODS file - 
named 'summary.ODS'.
