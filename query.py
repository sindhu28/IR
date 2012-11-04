from bs4 import BeautifulSoup
import urllib2
import urllib


query = raw_input('Enter term : ')
while query.lower() != "zzz":
    #enter the query
    if ' ' in query:
        print "enter a single term"
        continue 
    word = query.lower()
    #search the query in the index record of the urls
    f = open('D:/hw/metadata.txt', 'r')
    pages = []
    index = 0
    for line in f.readlines():
        values = dict(item.split(':',1) for item in line.split('(FIELD)',4))
        text = values['ANCHOR TEXT']
        if word in text:
            url = values['URL']
            pagerank = values['PAGE RANK']
            title = values['TITLE']
            pages.append([url, title, float(pagerank)])
    #sort the index records in order of page ranks
    pages.sort(key=lambda x:x[2], reverse=True)
    print len(pages)
    f.close()
    #Print snippet from the urls
    for page in pages:
        print page
        #print "\nURL:", page[0]
        #print "TITLE:", page[1]
        #print "PAGERANK", page[2]
        url = page[0]
        html = urllib2.urlopen(url)
        soup = BeautifulSoup(html)
        text_parts = soup.findAll(text=True)
        text = ''.join(text_parts)
        text = text.replace('\n', ' ')
        text = ' '.join(text.split())
        text = text.split()
        text = text[800:810]
        text = ' '.join(text)
        #print "CONTENT", text
    query = raw_input('Enter term : ')
