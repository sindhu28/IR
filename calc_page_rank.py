f = open('D:/Metadata.txt', 'r')
pages = []
oldpages = []
for line in f.readlines():
        values = dict(item.split(':',1) for item in line.split('(FIELD)',4))
        url = values['URL']
        pagerank = values['PAGE RANK']
        title = values['TITLE']
        ID = values['ID']
        pages.append((url, title, ID, int(pagerank)))
        oldpages.append([url, title, ID, int(pagerank)])
pages.sort(key=lambda x:x[3])        
for page in pages:
    print page[2].rjust(4), "  ",page[0]

index = 1
for page in pages:
    for opage in oldpages:
            if page[0]==opage[0]:
                    opage[3] = index
    index += 1
