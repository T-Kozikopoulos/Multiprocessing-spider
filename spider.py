from multiprocessing import Pool
import bs4 as bs
import random
import requests
import string


# Get a random 3 letter url.
def random_starting_url():
    starting = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(3))
    url = ''.join(['http://', starting, '.com'])
    return url


# Turn local pointers into full links so we can deal with them more easily.
def handle_local_links(url, link):
    if link.startswith('/'):
        return ''.join(([url, link]))
    else:
        return link


# Grab all the links.
def get_links(url):
    
    try:
        response = requests.get(url)
        soup = bs.BeautifulSoup(response.text, 'lxml')
        body = soup.body
        links = [link.get('href') for link in body.find_all('a')]
        links = [handle_local_links(url, link) for link in links]
        links = [str(link.encode("ascii")) for link in links]
        return links
    
    except TypeError as e:
        print(e)
        print('Got a TypeError, probably an empty website')
        return []
    
    except IndexError as e:
        print(e)
        print('IndexError, probably no useful links')
        return []
    
    except AttributeError as e:
        print(e)
        print('Got AttributeError, probably got None for links')
        return []
    
    # Got an unexpected error.
    except Exception as e:
        print(str(e))
        return []


def main():
    # Number of processes we want to run.
    how_many_processes = 20
    p = Pool(processes=how_many_processes)

    # Crawl a different url with each process.
    parsing_targets = [random_starting_url() for _ in range(how_many_processes)]
    data = p.map(get_links, [link for link in parsing_targets])

    # Take the data from all the lists and put it into one big list.
    data = [url for url_list in data for url in url_list]
    p.close()

    # Create a text file with all the links we got.
    with open('urls.txt', 'w') as f:
        f.write(str(data))


if __name__ == '__main__':
    main()
