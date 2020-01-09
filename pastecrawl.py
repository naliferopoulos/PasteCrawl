import requests
import time
from bs4 import BeautifulSoup

while True:
    # Links to crawl
    links = []
    
    try:

        # Fetch the page and parse it
        page = requests.get("http://pastebin.com/archive")
        soup = BeautifulSoup(page.content, 'html.parser')
    
        # Fetch the main table
        table = soup.find('table', {'class': 'maintable'})

        # Fetch the rows
        rows = table.findAll('tr')

        for tr in rows:
            # Fetch the columns
            cols = tr.findAll('td')

            for td in cols:
                # Fetch the links    
                hrefs = td.findAll('a')
                
                for a in hrefs:
                    # Fetch the content    
                    link = a.get('href')
                    
                    # Skip over default ones
                    if "archive" not in link:
                        links.append(link) 
    except:
        print("Failed to fetch latest content. Potential timeout by service. This may indicate a temporary ban!")
        break

    # Crawl each link
    for link in links:
        print("--> " + link)
        try:
            crawl = requests.get("http://pastebin.com/raw" + link)
            with open('./crawls/' + str(int(time.time())) + ".txt", "w") as f:
                f.write(crawl.text)
        except:
            pass

        time.sleep(10)


    time.sleep(10)
