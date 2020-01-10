import requests
import time
from bs4 import BeautifulSoup
import tagmaster
import signal
import inspect
import sys
import codecs

# ANSI Colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# The blacklisted words
blacklist = []

# The whitelisted words
whitelist = []

# Shoudl we exit?
should_exit = False

# An exception for blacklisted words
class BlacklistedWordException(Exception):
    pass

# Parse the blacklist
with open('blacklist.txt', 'r') as f:
    [blacklist.append(line.strip()) for line in f.readlines()]

# Parse the whitelist
with open('whitelist.txt', 'r') as f:
    [whitelist.append(line.strip()) for line in f.readlines()]

# Load all tagger packages in the default directory
tagmaster.collect_taggers('taggers')

# Define a signal handler for SIGINT
def sigint_handler(sig, frame):
    signal.signal(signal.SIGINT, original_sigint)
    while True:
        sys.stdout.write('\r')
        sys.stdout.flush()
        print("")
        instruction = input("> ").strip()

        if instruction == "exit":
            sys.exit(1)

        elif instruction == "continue":
            signal.signal(signal.SIGINT, sigint_handler)
            break
        elif instruction == "taggers":
            for tagger in tagmaster.taggers:
                print(bcolors.WARNING + "--> " + bcolors.ENDC, end='')
                print(inspect.getfile(tagger))
                print("")
        elif instruction == "links":
            for link in links:
                print(bcolors.WARNING + "--> " + bcolors.ENDC, end='')
                print(link)
                print("")
        else:
            print("Unknown instruction.")

        signal.signal(signal.SIGINT, sigint_handler)



# Save the original signal handler
original_sigint = signal.getsignal(signal.SIGINT)

# Register it
signal.signal(signal.SIGINT, sigint_handler)



# Crawling loop
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
    except SystemExit:
        sys.exit(0)
    except:
        print("Failed to fetch latest content. Potential timeout by service. This may indicate a temporary ban!")
        break

    # Crawl each link
    for link in links:
        if should_exit:
            sys.exit(0)

        print(bcolors.WARNING + "--> " + bcolors.ENDC, end='')
        print(link, end='')
        try:
            # Fetch the content
            crawl = requests.get("http://pastebin.com/raw" + link)
            
            # The tag list
            tags = []

            # Run every tagger
            for tag in tagmaster.run_taggers(crawl.text):
                tags.append(tag)
            
            # Print any tags identified by taggers in a different color
            for word in tags:
                print(bcolors.OKBLUE + " [" + word + "] " + bcolors.ENDC, end='')

            # Loop through the whitelist
            for word in whitelist:
                # Skip over comments and empty lines
                if word and not word.startswith('#') and not word.startswith(' '): 
                    # Convert crawl to lowercase and check if word is contained
                    if word in crawl.text.lower():
                        print(bcolors.OKGREEN + " [" + word + "] " + bcolors.ENDC, end='')
                        # Tag it
                        tags.append(word)

            # Loop through the blacklist
            for word in blacklist:
                # Skip over comments and empty lines
                if word and not word.startswith('#') and not word.startswith(' '):
                    # Convert crawl to lowercase and check if word is contained 
                    if word in crawl.text.lower():
                        print(bcolors.FAIL + " [" + word + "] " + bcolors.ENDC, end='')
                        # Bail out early
                        raise BlacklistedWordException("Blacklisted word!")

            # Prepend an empty tag if the list is not empty for cosmetic purposes
            if len(tags) > 0:
                tags.insert(0, '')

            # Write the crawel to the file, appending the timestamp and tag list to the filename
            with codecs.open('./crawls/' + str(int(time.time())) + '_'.join(tags) + ".txt", "w", encoding="utf-8") as f:
                f.write(crawl.text)
            
            # Sleep
            time.sleep(10)

        except SystemExit:
            sys.exit(0)
        except BlacklistedWordException:
            pass
        except Exception as e:
            print(e)

        # Advance to the next line
        print("")

    # Sleep
    time.sleep(10)
