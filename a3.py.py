#!/usr/bin/python
from numpy import *
from bs4 import BeautifulSoup
import urllib2
import re
from urlparse import urljoin
import unicodedata
import xml
import xml.etree.ElementTree

def process_url(url):
    #If there are anchors, just store the address of the page
    #print url
    tokens = url.split('/')
    
    if tokens[-1].find('#') == True:
        print "remove #"
        tokens[-1] = tokens[-1].split('#')[0]
        url = '/'.join(tokens)

    #if link contains default index.html, store only the rel addr to the dir
    tokens = url.split('/')
    if tokens[-1].startswith('index'):
        #print "remove index"
        tokens.remove(tokens[-1])
        url = '/'.join(tokens)+'/'
        #print url
    else:
        url = '/'.join(tokens)
    return url


def main():
    testdata = urllib2.urlopen("http://www.infosci.cornell.edu/Courses/info4300/2012fa/test/test3.txt")
    #testdata = open("C:/url.txt")
    testurllist = re.split(r"[\n|\r+]",testdata.read())
    urls = []
    links = 0
    urlID = []
    for testurl in testurllist:
        value = testurl.split(',')
        url = value[1]
        if len(url) != 0:
            #processing the urls to handle the case of # and /index which refer to the same links
            url = process_url(url)
            if url not in urls:
                urls.append(url)
                urlID.append(value[0])
                links += 1
       
    cited_citing_array = zeros(shape=(links,links))

    print "crawling to find links: please wait"
    
    out_pagelinks = []
    for idx in range(0,links):
        out_pagelinks.append([])
    in_pagelinks = []
    for idx in range(0,links):
        in_pagelinks.append([])
    dangling_links = []
    title_tags = []

    #contructing the cited citing matrix
    for url in urls:
        col = urls.index(url)
        htmlpage = urllib2.urlopen(url)
        soup = BeautifulSoup(htmlpage)
        title_tag = soup.find('title').renderContents()
        title_tag = title_tag.replace('\n',' ')
        title_tags.append(title_tag)
        #finding all <a> tags
        for link in soup.findAll('a'):
            pagelink = link.get('href')
            if pagelink != None:
                #processing the urls to find absolute addresses from relative addresses
                pagelink = urljoin(url, pagelink)
                #processing the urls to handle the case of # and /index which refer to the same links
                pagelink = process_url(pagelink)
                if pagelink in urls:
                    row = urls.index(pagelink)
                    if row == col:
                        #ignoring links from a url to itself
                        cited_citing_array[row][col] = 0
                    else:
                        #add an entry for a link from an url only once and ignore if duplicate
                        if cited_citing_array[row][col] == 0:
                            cited_citing_array[row][col] = 1
                            out_pagelinks[col].append(pagelink)
                        #finding inlinks for all urls
                        anchor = link.contents
                        anchorText = ''
                        if anchor:
                            try:
                                anchorText = anchor[0].encode('ascii', 'ignore')
                            except TypeError:
                                root = xml.etree.ElementTree.fromstring(str(anchor[0]))
                                if root.tag == 'img':
                                    attributes = root.attrib
                                    if 'alt' in attributes.keys():
                                        anchorText = attributes['alt']   
                                else:
                                    anchorText =  ''.join(xml.etree.ElementTree.fromstring(str(anchor[0])).itertext())
                        anchorText = anchorText.strip()
                        anchorText = anchorText.replace('\n', ' ')
                        anchorText = " ".join(anchorText.split())
                        in_pagelinks[col].append([url, anchorText])
        #finding links without any outlinks
        if len(out_pagelinks[col]) == 0:
            dangling_links.append(col)

    print "crawling done"

    #finding outlinks for all urls
    total = 0
    out_links = []
    for col in range(0,links):
        count = 0
        for row in range(0,links):
            count += cited_citing_array[row][col]
        out_links.append([urls[col], count])
        print "col", col, ":", count
        total += count
    print total
    
    #normalizing
    for col in range(0,links):
        for row in range(0,links):
            if out_links[col][1] != 0 :
                cited_citing_array[row][col] = ((cited_citing_array[row][col]/out_links[col][1]))
    
    #(1-d)R
    R = zeros(shape=(links,links))
    for row in range(0,links):
        for col in range(0,links):
            if out_links[row][1] != 0:
                R[row][col] = 0.15/links
            
    #G = dB + (1-d)R             
    for row in range(0,links):
        for col in range(0,links):
            cited_citing_array[row][col] =  ((cited_citing_array[row][col]*0.85 + R[row][col]))

    #initializing w 
    w = zeros(shape=(links,1))
    wk1 = w
    for row in range(0,links):
        w[row][0] = 1
    wk2 = dot(cited_citing_array,w)
   
    #w(k2) = dBw(k1) till it converges
    itr = 0
    while allclose(wk1, wk2) == False:
        wk1 = wk2
        wk2 = dot(cited_citing_array,wk1)
        itr += 1
    print itr

    fw = open('D:/hw/metadata.txt', 'w')
    for row in range(0,links):
        string = ""
        for val in in_pagelinks[row]:            
            #string = string+'(url):'+val[0]+"-"+'(anchor text):'+val[1]+" "
            string = string + val[1].lower()+" "
        data = 'ID:'+urlID[row]+'(FIELD)'+'URL:'+urls[row]+'(FIELD)'+'TITLE:'+title_tags[row]+'(FIELD)'+'PAGE RANK:'+str(wk1[row][0])+'(FIELD)'+'ANCHOR TEXT:'+string+'\n'
        fw.writelines(data)
    fw.close()

if __name__ == "__main__":
    main()
