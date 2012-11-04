f = open('D:/hw/metadata.txt', 'r')
pages = []
oldpages = []
for line in f.readlines():
        values = dict(item.split(':',1) for item in line.split('(FIELD)',4))
        url = values['URL']
        pagerank = values['PAGE RANK']
        title = values['TITLE']
        ID = values['ID']
        pages.append((url, title, ID, float(pagerank)))
        oldpages.append((url, title, ID, float(pagerank)))
pages.sort(key=lambda x:x[3], reverse=True)        
for page in pages:
    print page[2].rjust(4), "  ",page[0]
