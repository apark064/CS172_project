from bs4 import BeautifulSoup  # install BeautifulSoup4
import requests  # install requests and lxml
import pandas as pd

def robot(url): # returns disallowed contents
    robots_url = url + '/robots.txt'
    print(robots_url)
    robots = requests.get(robots_url).text
    data = []
    lines = str(robots).splitlines()
    #print(lines)
    for line in lines:

        if line.strip():
            if not line.startswith('#'):
                split = line.split(':', maxsplit=1)
                if(split[0].strip() == 'Disallow'):
                    data.append([split[1].strip()])
    #print(pd.DataFrame(data, columns=['parameter']))
    return pd.DataFrame(data, columns=['parameter'])

def crawler(seed, num_page, num_level):
    seed_url = seed
    source = requests.get(seed_url).text
    queue = []
    iter_page = 1  # queue.len()
    iter_level = 1 # depth from seed_url
    queue.append(seed_url)
    disallowed = robot(seed)
    while queue and iter_level < num_level:
        iter_level += 1
        # get all url and put them in the queue (beautiful soup)
        soup = BeautifulSoup(source, 'lxml')
        for url in soup.find_all('a', href=True):  # need to fix
            if url not in disallowed: # avoid disallowed contents from robots.txt
                if iter_page < num_page:
                    if url not in queue:  # URL Duplicate Reduction
                        if 'http' in url.get('href'):
                            queue.append(url.get('href'))
                            iter_page += 1
        # elastic search

    print(queue)

seed_url = 'https://www.ucr.edu'
crawler(seed_url, 20, 2)
#robot(seed_url)