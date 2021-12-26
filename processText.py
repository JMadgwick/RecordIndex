import sys
import os
import re
import unidecode

def readtxtfile(filepath):
    f = open(filepath, "r")
    text = unidecode.unidecode(f.read())#Unidecode - https://stackoverflow.com/a/2633310
    text = text.replace('"','').replace("'",'')
    f.close()
    return text

def findlabel(txtlist):
    txtlist = txtlist.lower()
    txt = txtlist.replace("\n"," ")
    hmv=re.search("master.{0,5}voice", txt)
    decca=re.search("d.?e.?c.?c.?a", txt)
    london=re.search("london.{0,5}american", txt)
    mgm=re.search("m.?g.?m", txt)
    fourtune=re.search("broadcast.?four", txt)

    if "brunswick" in txt:
      return "Brunswick"
    elif "regal" in txt:
      return "Regal"
    elif "filmophone" in txt:
      return "Filmophone"
    elif "columbia" in txt:
      return "Columbia"
    elif "the king of records" in txt:
      return "Rex"
    elif "philips" in txt:
      return "Philips"
    elif "parlophone" in txt:
      return "Parlophone"
    elif ("capitol" in txt):
      return "Capitol"
    elif ("vocalion" in txt):
      return "Vocalion"
    elif (type(hmv) != type(None)) or ("master's" in txt) or ("his master" in txt):
      return "His Master's Voice"
    elif type(decca) != type(None):
      return "Decca"
    elif type(london) != type(None):
      return "London American Recordings"
    elif type(mgm) != type(None):
      return "MGM"
    elif "sterno" in txt:
      return "Sterno"
    elif "odeon" in txt:
      return "Odeon"
    elif "embassy" in txt:
      return "Embassy"
    elif "zonophone" in txt:
      return "Zonophone"
    elif type(fourtune) != type(None):
      return "Broadcast Four-Tune"
    elif "imperial" in txt:
      return "Imperial"
    elif ("nixa" in txtlist) or ("mxa" in txtlist):
      return "Nixa"
    elif ("rca" in txtlist):
      return "RCA"
    elif ("pathe" in txtlist):
      return "Pathe"
    else:
      return "Unknown"

def findcatmatrix(txt):
    found = []
    for line in txt.split("\n"):
        found.extend(re.findall(".*\d{3,}.*",line))
    return found

def tidytext(txt):
       return txt.replace("\n"," ")[:-24]

def recnum(item):
    return int(item.split("_")[1][:-6])

def findbside(num):
    bside = [item for item in records_sideb if str(num) == item.split("_")[1][:-6]]
    if len(bside) != 0:
        return bside[0]
    return "No File"

def catguess(a,b):
    a = [item.replace('.','').replace('-A','').replace('-B','').replace('-','').replace(':','').replace(',','').replace(' ','') for item in a]
    b = [item.replace('.','').replace('-A','').replace('-B','').replace('-','').replace(':','').replace(',','').replace(' ','') for item in b]
    return [item for item in a if b.count(item) > 0]

path = os.getcwd() + '/' + sys.argv[1]

ls = os.listdir(path)
records = [item for item in ls if "A.txt" in item]#https://realpython.com/list-comprehension-python/
records.sort(key=recnum)
records_sideb = [item for item in ls if "B.txt" in item]
records_sideb.sort(key=recnum)

csv = '"Reference"\t"Company"\t"Possible Cat #"\t"Numbers 1"\t"Image 1"\t"Numbers 2"\t"Image 2"\t"Language"\t"Text 1"\t"Text 2"\n'

for record in records:
    #Side 1
    asidepath = path + '/' + record
    txt_1 = readtxtfile(asidepath)
    catmatrix_1 = findcatmatrix(txt_1)
    label = findlabel(txt_1)
    lang = txt_1.split("\n")[-1][-2:]

    ref = record[:-6]
    
    #Side 2
    bsidepath = path + '/' + findbside(recnum(record))
    if os.path.isfile(bsidepath): 
        txt_2 = readtxtfile(bsidepath)
        catmatrix_2 = findcatmatrix(txt_2)
        if label == "Unknown": label = findlabel(txt_2)
    else:
        txt_2 = ""
        catmatrix_2 = ""

    guessedCat = catguess(catmatrix_1,catmatrix_2)
    txt_1 = tidytext(txt_1)
    txt_2 = tidytext(txt_2)
    img1 = '=HYPERLINK("./' + sys.argv[1] + "/" + record[:-3] + 'jpg","' + record[:-4] + '")'
    img2 = '=HYPERLINK("./' + sys.argv[1] + "/" + record[:-5] + 'B.jpg","' + record[:-5] + 'B")'
    csv += '"' + ref + '"\t"' + label + '"\t"' + ", ".join(guessedCat) + '"\t"' + ", ".join(catmatrix_1) + '"\t"' + img1 + '"\t"' + ", ".join(catmatrix_2) + '"\t"' + img2 + '"\t"' + lang +'"\t"' + txt_1 + '"\t"' + txt_2 + '"'
    csv += '\n'

csvfile = os.getcwd() + '/' + "Index for " + sys.argv[1] + ".tsv"
print(csvfile)
out = open(csvfile, "w")
out.write(csv)
out.close()
