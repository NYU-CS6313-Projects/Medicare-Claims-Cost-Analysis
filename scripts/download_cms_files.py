import lxml.html
import urllib2
import requests
import urllib

r = requests.get("http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/DE_Syn_PUF.html")
html = lxml.html.fromstring(r.text)
links_main = html.xpath("//a[contains(text(),'DE1')]")
base = 'http://www.cms.gov'

cnt = 10 

for i in links_main:
    appendURL = i.get("href")
    newURL = base + appendURL
    r = requests.get(newURL)
    html = lxml.html.fromstring(r.text)
    links = html.xpath("//a[contains(@href,'DE1_')]")
    
    for i in links:
        if "downloads.cms.gov" in i.get("href"):
            location =  i.get("href")
            zipfilename = "zip" + str(cnt) + ".zip"
            urllib.urlretrieve(location, zipfilename)
            print "downloading.....%s" % zipfilename
        else:
            location = base+i.get("href")
            zipfilename = "zip" + str(cnt) + ".zip"
            urllib.urlretrieve(location, zipfilename)
            print "downloading.....%s" % zipfilename

        cnt += 1
