from math import ceil
import pysmashgg
import challonge
import os
from dotenv import load_dotenv

load_dotenv()
challonge.set_credentials(os.getenv('CHALLONGE_USER'), os.getenv('CHALLONGE_KEY'))
smash = pysmashgg.SmashGG(os.getenv('STARTGG_KEY'))

# Process URLs

def trimHTTP(url):
    '''
    Trim HTTP/HTTPS/WWW out of url strings
    '''
    WASTE = ['https://', 'http://', 'www.']
    trimmed = url
    for term in WASTE:
        if term in trimmed:
            trimmed = url[len(term):]
    # print(f"\n{trimmed}\n  from\n{url}")
    return trimmed

def url_challonge(url):
    '''
    Pick apart a Challonge URL to get the important bits
    '''
    trimmed = trimHTTP(url)
    domainStart = trimmed.find('challonge.com/')
    if domainStart == -1:
        return ["",""]
    if domainStart == 0:
        return ["", trimmed.split('/')[1]]
    return [trimmed[ : domainStart-1 ], trimmed.split('/')[1]]

def url_startgg(url):
    '''
    Pick apart a StartGG URL for the important bits
    '''
    trimmed = trimHTTP(url)
    domainStart = trimmed.find('start.gg/tournament/')
    if domainStart == -1:
        domainStart = trimmed.find('smash.gg/tournament/')
    if domainStart == -1:
        return ["",""]
    trimmed = trimmed[ domainStart + len('start.gg/tournament/') : ]
    x = trimmed.split('/event/')
    print(x)
    y = x[1].split('/')
    return [x[0], y[0]]
    
# Make API calls

def flattenList(old):
    lst = list()
    for sub_list in old:
        lst += sub_list
    return lst

def unFlatListtoDict(a):
    # print(a)
    lst = flattenList(a)
    it = iter(lst)
    res_dct = dict(zip(it, it))
    return res_dct

def DictToList(dct):
    lst2 = []
    for i in range(1, len(list(dct))+1):
        # print(i, dct[i])
        lst2.append(dct[i])
    return lst2

def partName(part):
    if(part['name'] == ''): return part['display_name']
    return part['name']

def partName2(part):
    return [part['seed'], part['name']]

def partTag(part):
    return [part['seed'], part['entrantPlayers'][0]['playerTag']]

def unordered_challonge(org, slug):
    if (org == ""):
        participants = challonge.participants.index(slug)
    else:
        participants = challonge.participants.index(f"{org}-{slug}")
    result = map(partName2, participants)
    return result

def entrants_challonge2(url):
    [org, slug] = url_challonge(url)
    lst = unordered_challonge(org, slug)
    dct = unFlatListtoDict(lst)
    return DictToList(dct)

def entrants_challonge(org, slug):
    if (org == ""):
        participants = challonge.participants.index(slug)
    else:
        participants = challonge.participants.index(f"{org}-{slug}")
    result = map(partName, participants)
    return list(result)

def entrants_challongeurl(url):
    [org, slug] = url_challonge(url)
    return entrants_challonge(org, slug)

def unordered_startgg(tourney, event):
    num_entrants = smash.tournament_show(tourney)['entrants']
    # print(f"{num_entrants} entrants, {1+ceil(num_entrants/25)} pages")

    result = []
    for page_num in range(1, 1+ceil(num_entrants/25)):
        page = smash.tournament_show_entrants(tourney, event, page_num)
        add = list(map(partTag, page))
        # print(f"page {page_num}: {add}")
        if len(add) == 0:
            # print(f"length {len(list(result))}: {result}")
            return result
        result += add
    # print(f"length {len(list(result))}: {result}")
    return result

def entrants_startgg(tourney, event):
    lst = unordered_startgg(tourney, event)
    dct = unFlatListtoDict(lst)
    return DictToList(dct)

def entrants_startggurl(url):
    [tourney, event] = url_startgg(url)
    return entrants_startgg(tourney, event)