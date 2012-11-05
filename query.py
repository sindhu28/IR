from bs4 import BeautifulSoup, Comment
import urllib2
import urllib


query = raw_input('Enter term : ')
while query.lower() != "zzz":
    #enter the query
    if ' ' in query:
        print "enter a single term"
    else:
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
                ID = values['ID']
                pages.append([url, title, float(pagerank), ID])
        #sort the index records in order of page ranks
        pages.sort(key=lambda x:x[2], reverse=True)
        f.close()
        #Print snippet from the urls
        index = 0
        for page in pages:
            url = page[0]
            html = urllib2.urlopen(url)
            soup = BeautifulSoup(html)
            ptext = soup.findAll('div')
            string=''
            for line in ptext:
                text = line.findAll(text=True, )
                text = ''.join(text)
                text = text.replace('\n', ' ')
                text = ' '.join(text.split())+' '
                string = string+text+' '
            string = string.split()
            l = len(string)
            mid = l/2
            if (l/2+20) < l:
                string = string[mid:mid+20]
            else:
                string = string[mid:]
            string = ' '.join(string)           
            print '\n',page[0]
            print "TITLE:", page[1]
            print "CONTENT:", string
    query = raw_input('\nEnter term : ')
