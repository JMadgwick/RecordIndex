import os
from pyexcel_ods3 import get_data as import_ods_data
from pyexcel_ods3 import save_data as export_ods_data
from collections import OrderedDict

def filenum(item):
    return int(item.split("_")[1][:-4])

ls = os.listdir(os.getcwd())
files = [item for item in ls if "Discogs" in item]#https://realpython.com/list-comprehension-python/
files.sort(key=filenum)

rows = [['Reference', 'Label', 'Checked Cat #', '', 'Box Number', 'Discogs Title', 'Release URL', 'Master URL', 'Other Release URLs']]

for filename in files:
    sheetName = filename[8:-4]
    odfData = import_ods_data(filename)

    #Remove first line
    odfData[sheetName].reverse()
    odfData[sheetName].pop()
    odfData[sheetName].reverse()

    #Add Box number
    for line in odfData[sheetName]:
        line.insert(4, filename[22:-4])

    #Sometimes there are blank rows (empty list) in the sheet which cause index out of range, don't add these
    rows.extend([item for item in odfData[sheetName] if item!=[]])

odfDataOut = OrderedDict()
odfDataOut.update({"Sheet 1": rows})
export_ods_data("Summary.ods", odfDataOut)
