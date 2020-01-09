import requests
import time
from bs4 import BeautifulSoup

while True:
    # Links to crawl
    links = []

    # Fetch the page and parse it
    page = requests.get("http://pastebin.com/archive")
    soup = BeautifulSoup(page.content, 'html.parser')

    # Fecth the main table
    table = soup.find('table', {'class': 'maintable'})

    # Fetch the rows
    rows = table.findAll('tr')

    for tr in rows:
        #print("\tFound Row")
        # Fetch the columns
        cols = tr.findAll('td')

        for td in cols:
            #print("\t\tFound Column")
            # Fetch the links    
            hrefs = td.findAll('a')
            
            for a in hrefs:
                #print("\t\t\tFound Link")
                # Fetch the content    
                link = a.get('href')
                
                # Skip over default ones
                if "archive" not in link:
                    links.append(link) 
    
    # Crawl each link
    for link in links:
        print("--> " + link)
        try:
            crawl = requests.get("http://pastebin.com/raw" + link)
            #with open('./crawls/' + link + '_' + str(int(time.time())) + ".txt", "w") as f:
            with open('./crawls/' + str(int(time.time())) + ".txt", "w") as f:
                f.write(crawl.text)
        except:
            pass

        time.sleep(10)


    time.sleep(10)
