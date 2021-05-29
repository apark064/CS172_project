from bs4 import BeautifulSoup  # install BeautifulSoup4
import requests  # install requests and lxml

def crawler(num_page, num_level):
    source = requests.get('http://ucr.edu').text
    seed_url = 'http://ucr.edu'
    queue = []
    iter_page = 1  # queue.len()
    iter_level = 1 # depth from seed_url
    queue.append(seed_url)
    while queue and iter_level < num_level:
        iter_level += 1
        # get all url and put them in the queue (beautiful soup)
        soup = BeautifulSoup(source, 'lxml')
        for url in soup.find_all('a', href=True):  # need to fix
            #print(url['href'])
            if iter_page < num_page:
                iter_page += 1
                if url not in queue:  # URL Duplicate Reduction
                    queue.append(url.get('href'))
        # elastic search

    print(queue)

crawler(20, 2)