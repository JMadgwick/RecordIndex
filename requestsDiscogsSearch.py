import requests,time,sys
from pyexcel_ods3 import get_data as import_ods_data
from pyexcel_ods3 import save_data as export_ods_data

filename = str(sys.argv[1])
sheetName = filename[:-4]
odfData = import_ods_data(filename)
#Sometimes there are blank rows (empty list) in the sheet which cause index out of range, remove these
odfData[sheetName] = [item for item in odfData[sheetName] if item!=[]]#https://realpython.com/list-comprehension-python/

rHeader = {'user-agent': 'RecordIndexer/0.1', 'Accept': 'application/vnd.discogs.v2.discogs+json', 'Authorization': 'Discogs token='}

def dcAPIcall(label, catno, country):
    response = requests.get('https://api.discogs.com/database/search?type=release&country=%s&label=%s&catno=%s' % (country,label,catno),headers=rHeader)
    return response.json().get('results')

def catSearch(country,label,catNo):
    catNo = str(catNo).replace('.','').replace('-','').replace(' ','').lower()
    searchResults = dcAPIcall(label=label, country=country, catno=catNo)
    possibleHits = []
    masterIDs = []
    for record in searchResults:
        cat = record['catno'].replace('.','').replace('-','').replace(' ','').lower()
        master = record['master_id']
        #If exact(ish) match and master not found already
        if (cat==catNo or cat==('0'+catNo)) and master not in masterIDs:#TODO "'78 RPM' in format" check
            masterIDs.append(master)
            possibleHits.append(record)
    return possibleHits

odfData[sheetName][0] = ['Reference', 'Label', 'Checked Cat #', '', 'Discogs Title', 'Release URL', 'Master URL', 'Other Release URLs']
for sheetRow in range(1, len(odfData[sheetName])):
    ref = odfData[sheetName][sheetRow][0]
    label = odfData[sheetName][sheetRow][1]
    cat = odfData[sheetName][sheetRow][2]
    country = odfData[sheetName][sheetRow][7]
    #if country == 'en': country='uk' #language -> country (This has issues due to uk records misidentified as foreign)
    results = catSearch('uk',label,cat)#catSearch(country,label,cat)
    time.sleep(2)
    if len(results) != 0:
        releaseURL = 'discogs.com/release/' + str(results[0]['id'])
        odfData[sheetName][sheetRow] = [ref,label,cat,'',results[0]['title'],releaseURL]
        if results[0]['master_id'] > 0:
            masterURL = 'discogs.com/master/' + str(results[0]['master_id'])
            odfData[sheetName][sheetRow].append(masterURL)
        else:
            odfData[sheetName][sheetRow].append('N/A')
        for possibleHit in results:
            if possibleHit['title'] != results[0]['title']:
                otherURL = 'discogs.com/release/' + str(possibleHit['id'])
                odfData[sheetName][sheetRow].append(otherURL)
    else:
        odfData[sheetName][sheetRow] = [ref,label,cat,'','Not Found']

export_ods_data("Discogs " + filename, odfData)
