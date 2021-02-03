#########################################################
###  Functions to get articles from BBC News            #
#########################################################

import requests
from bs4 import BeautifulSoup

def getHeadlineURLs():
    x = requests.get('https://www.bbc.co.uk/news')
    soup = BeautifulSoup(x.text, features="html.parser")

    links = soup.find("div", {"aria-label": "Top Stories"}).find_all("a")

    [s.extract() for s in soup('span')]
    [s.extract() for s in soup('svg')]

    links = links[5:]

    for tag in soup():
        for attribute in ["class"]: # You can also add id,style,etc in the list
            del tag[attribute]

    href = []
    for link in links:
        fullLink = "http://bbc.com" + link["href"]
        if link["href"] != "":
            if fullLink not in href:
                href.append(fullLink)
    return href

def getArticleInfo(url):
    x = requests.get(url)
    soup = BeautifulSoup(x.text, features="html.parser")

    template = {
        "title": "",
        "subheading": "",
        "url": url
    }

    template["title"] = soup.find("h1", {"id": "main-heading"}).text
    template["subheading"] = soup.find_all("p")[0].text + soup.find_all("p")[1].text + soup.find_all("p")[2].text

    return template

def getArticles():
    URLs = getHeadlineURLs()
    articles = []

    for url in URLs:
        try:
            article = getArticleInfo(url)
            if article not in articles:
                ##print(article)
                articles.append(article)
        except:
            pass

    return articles

print(getArticles())