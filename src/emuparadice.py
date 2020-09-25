import re

import requests
from bs4 import BeautifulSoup


def get_data(url):
    """Get HTML data from a site
    args:
        url: the url to the site we're scraping
    """

    try:
        r = requests.get(url)
    except Exception as e:
        raise e
    else:
        print('Scrape success')

    try:
        # convert html to a BeautifulSoup Object
        bs = BeautifulSoup(r.text, 'html.parser')
    except Exception as e:
        raise e

    try:
        # find all <a> tages that link to a game
        endpoints = bs.find_all('a', {'class', 'gamelist'})
    except AttributeError as e:
        raise AttributeError('Invalid attribute')
    except Exception as e:
        raise e

    return endpoints


def filter_endpoints(endpoints):
    """Remove unwanted links from the list
    args:
        endpoints: the list of endpoints received from the scrape
    """

    filtered = []
    trash_reg = re.compile(r'(japan|Japan|\(j\)|\(J\)|germany|German|\(g\)|\(G\)|\(s\)|\(S\)|\(f\)|\(F\)|Essential_PlayStation|Interactive_CD_Sampler|PlayStation_Underground_|PlayStation_Picks|_Magazine_|Official_PlayStation_|Official_UK_PlayStation_|_Demo_)')

    # iterate over the list of endpoints and check against the regular
    # expression above. If no match is found, add the endpoint to the
    # filtered list.
    for e in endpoints:
        match = trash_reg.search(e.get('href'))
        if not match:
            filtered.append(e.get('href'))

    return filtered


def get_game_ids(endpoints):
    """Split each enpoint down to its unique game id and append
    the ID to a new array
    args:
        endpoints: the filtered list of game endpoints
    """

    ids = []

    for e in endpoints:
        arr = e.split('/')
        ids.append(arr[-1])

    return ids


def build_download_links(game_ids):
    """Make download links for each game ID
    args:
        game_ids: The list of ids stripped from each endpoint
    """

    # site = 'http://50.7.189.186/'
    site = 'http://www.emuparadise.me/'

    download_links = []

    for id in game_ids:
        download_url = f"{site}roms/get-download.php?gid={id}&test=true"
        download_links.append(download_url)

    return download_links


games = get_data(
    url='https://www.emuparadise.me/Sony_Playstation_ISOs/List-All-Titles/2')

filtered = filter_endpoints(endpoints=games)
for f in filtered:
    print(f)
print(f"total: {len(filtered)}")

game_ids = get_game_ids(endpoints=filtered)

links = build_download_links(game_ids=game_ids)
for l in links:
    print(l)
print(f"total: {len(links)}")
