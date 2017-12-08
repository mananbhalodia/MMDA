
import urllib.request as urlib
import urllib.error as urlibError
from bs4 import BeautifulSoup
import html5lib

# In[57]:


def extractmeta (url2):
    try:
        webpage = urlib.urlopen(url2).read()
        soup = BeautifulSoup(webpage, "html5lib")
        meta = soup.findAll("meta")
        count = 0
        size = 3
        location, title, doctype, pubdate, lastmod, author, keywords, category,url = [],[],[],[],[],[],[],[],[]
        location = url2
        if (soup.findAll("meta",  {"name":"author"})):
            author = soup.findAll("meta",  {"name":"author"})[0]['content'];
        if (soup.findAll("meta",  property="og:title")):
            title = soup.findAll("meta",  property="og:title")[0]['content']
        if (title == []) :
            if (soup.find("title")):
                title = soup.find("title").get_text()
        if (soup.findAll ("meta", {"charset":True})):
            doctype = soup.findAll ("meta", {"charset":True})[0]['charset']
        if (soup.findAll("meta",  property="og:pubdate")):
            pubdate = soup.findAll("meta",  property="og:pubdate")[0]['content']
        if (soup.findAll("meta",  {"name":"lastmod"})):
            lastmod = soup.findAll("meta",  {"name":"lastmod"})[0]['content']
        if (soup.findAll("meta",  {"name":lambda L: L and "keyword" in L})):
            keywords = soup.findAll("meta",  {"name":lambda L: L and "keyword" in L})[0]['content'].split()
        if (soup.findAll("meta",  {"name":"description"})) :
            keywords.extend(soup.findAll("meta",  {"name":"description"})[0]['content'].split())
        if (soup.findAll("meta",  property="og:type")):
            category = soup.findAll("meta",  property="og:type")[0]['content']
        if (soup.findAll("meta",  property= lambda L: L and "url" in L)):
            for u in (soup.findAll("meta",  property= lambda L: L and "url" in L)) :
                check = u["content"]
                if (check.startswith("http")):
                    url.append(check)
                    count += 1
                    if (count >= size):
                        break
        if (soup.findAll("link") and count < size) :
            temp = soup.findAll("link")
            for u in temp:
                if (u.has_attr("href")):
                    if (u["href"]) :
                        if (u["href"].startswith("http")):
                            url.append(u["href"])
                            count += 1
                            if (count >= size):
                                break
        if (soup.findAll("a") and count < size) :
            temp = soup.findAll("a")
            for u in temp:
                if (u.has_attr("href")):
                    if (u["href"]) :
                        if (u["href"].startswith("http")):
                            url.append(u["href"])
                            count += 1
                            if (count >= size):
                                break
        meta = {
            "location": location,
            "title" : title,
            "doctype" : doctype,
            "pubdate" : pubdate,
            "lastmod" : lastmod,
            "author" : author,
            "keywords" : keywords,
            "category" : category,
            "url": url,
            "parent" : ""
        }
        return meta
    except urlibError.HTTPError:
        location, title, doctype, pubdate, lastmod, author, keywords, category,url = [],[],[],[],[],[],[],[],[]
        meta = {
            "location" : location,
            "title" : title,
            "doctype" : doctype,
            "pubdate" : pubdate,
            "lastmod" : lastmod,
            "author" : author,
            "keywords" : keywords,
            "category" : category,
            "url": url,
            "parent" : ""
        }
        return meta



# In[58]:


def multi (url):
    temp = extractmeta(url)
    temp["parent"] = "root"
    if (url in temp['url']):
        temp['url'].remove(url);
    og = []
    pc = []
    c2 = []
    og.append(temp)
    for u in temp['url'] :
        child = extractmeta(u)
        if (child["location"] in child['url']):
            child['url'].remove(child["location"]);
        child["parent"] = url
        if (child["title"] != [] and child["parent"] != child["location"]) :
            pc.append(child)
    for u in pc :
        for u2 in u["url"] :
            child = extractmeta(u2)
            if (u2 in child["url"]) :
                child["url"].remove(u2)
            child["parent"] = u["location"]
            if (child["title"] != [] and child["parent"] != child["location"]) :
                c2.append(child)
    pc.append(c2)
    og.append(pc)
    return og



# In[24]:
