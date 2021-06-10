#!/usr/bin/python3
from bs4 import BeautifulSoup  # install BeautifulSoup4
import requests  # install requests and lxml
import pandas as pd
import urllib.request
import json
from datetime import datetime
from time import sleep
from elasticsearch import Elasticsearch, helpers
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def robot(url):  # returns disallowed contents
    robots_url = url + '/robots.txt'
    # print(robots_url)
    robots = requests.get(robots_url).text
    data = []
    lines = str(robots).splitlines()
    # print(lines)
    for line in lines:
        if line.strip():
            if not line.startswith('#'):
                split = line.split(':', maxsplit=1)
                if (split[0].strip() == 'Disallow'):
                    data.append([split[1].strip()])
    # print(pd.DataFrame(data, columns=['parameter']))
    return pd.DataFrame(data, columns=['parameter'])


def crawler(seed, num_page, num_level):
    seed_url = seed
    source = requests.get(seed_url).text
    queue = []
    iter_page = 1  # queue.len()
    iter_level = 1  # depth from seed_url
    queue.append(seed_url)
    disallowed = robot(seed)
    while queue and iter_level < num_level:
        iter_level += 1
        # get all url and put them in the queue (beautiful soup)
        soup = BeautifulSoup(source, 'lxml')
        for url in soup.find_all('a', href=True):  # need to fix
            if url not in disallowed:  # avoid disallowed contents from robots.txt
                if iter_page < num_page:
                    if url not in queue:  # URL Duplicate Reduction
                        if 'http' in url.get('href'):
                            queue.append(url.get('href'))
                            iter_page += 1
        # elastic search
    return queue
    # print(queue)


def get_body_text(link):
    html = urllib.request.urlopen(link)
    page_soup = BeautifulSoup(html, "html.parser")
    if page_soup.main:
        body_soup = page_soup.main
    else:
        body_soup = page_soup
    containers = body_soup.find_all("p")
    str = ''
    for para in containers:
        str += para.get_text()
        str += '\n'
        # print(para.get_text())
    return str


def sort_list_by_time(list):  # make priority queue by last-updated-time. If not, append back in same order traversed
    # <head> .. <meta property="og:updated_time" content="2021-06-02T16:43:53-0700">
    p_queue = []
    list_without_update = []
    for item in list:
        html = urllib.request.urlopen(item)
        page_soup = BeautifulSoup(html, "html.parser")
        exist = page_soup.head.find("meta", property="og:updated_time")
        if exist:
            p_queue.append([exist["content"], item]) #time, url
            print(p_queue)
        else:
            list_without_update.append(item)

    p_queue = sorted(p_queue, key=lambda x: x[0], reverse=True)
    return_list = []
    for thing in range(len(p_queue)):
        return_list.append(p_queue[thing][1])

    return return_list + list_without_update

link = 'https://www.ucr.edu/'
list = crawler(link, 10, 2)
print(list)
print(sort_list_by_time(list))
print('end')

link = 'https://www.ucr.edu/'
link1 = 'https://news.ucr.edu/articles/2021/06/01/2021-voices-grads-share-pivotal-moments-their-educational-journeys'
# print(get_body_text(link1))


# ========================================

list = crawler(link, 10, 2) # seed, num_page, num_level
print('list :')
print(list)

elastic_pass = "HdEPP9nkrjsbs0fy7sb7Dztm"
elastic_endpoint = "i-o-optimized-deployment-753d85.es.us-west1.gcp.cloud.es.io:9243"


# "i-o-optimized-deployment-753d85.es.us-west1.gcp.cloud.es.io:9243"

connection_string = "https://elastic:" + elastic_pass + "@" + elastic_endpoint

indexName = "myindex_1"  # "cs172-index"
esConn = Elasticsearch(connection_string)
response = esConn.indices.create(index=indexName, ignore=400)  # create index
print(response)  # status


for link in list:
    url = link
    # title = "blah"
    text = get_body_text(link)
    # author = ""
    doc = {
            'url': url,  # url
            # 'page_title': title, # extract webpage name
            'text': text,  # html body text
            'timestamp': datetime.now()  # current date or maybe webpage date
            # 'author': author
    }
    # json_object = json.dumps(doc, indent=4)  #convert library to json obj
    response = esConn.index(index=indexName, id=id, body=doc)  # add doc to index
    print(response)  # result status

response = esConn.search(index=indexName, body={"query": {"match_all": {}}})
print(response)  # result status

# think this is how we look up a query?


query = "blah"
response = esConn.search(index=indexName, body={
        'query': {
            'match': {
                "text": query
            }
        }
    })

print(response)  # result status



#curl -X PUT -u elastic:HdEPP9nkrjsbs0fy7sb7Dztm "https://i-o-optimized-deployment-753d85.es.us-west1.gcp.cloud.es.io:9243/myindex?pretty"    <-- cretate "myindex"
#curl -X DELETE -u elastic:HdEPP9nkrjsbs0fy7sb7Dztm "https://i-o-optimized-deployment-753d85.es.us-west1.gcp.cloud.es.io:9243/myindex?pretty"    <-- delete "myindex"


