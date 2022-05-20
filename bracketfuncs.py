# Bracket Functions, utilities for manipulating brackets.
#
#

from collections import OrderedDict

def containsBye(match):
    p1bye = match.part1 and match.part1.isbye()
    p2bye = match.part2 and match.part2.isbye()
    return p1bye or p2bye


def projected(brackets):
    '''
    updates a bracket to reflect winnings by seeds.
    will mutate the bracket, so to keep original create a
    copy before calling
    '''
    for bracket in brackets:
        br = bracket
        while br != []:
            nbr = []
            for match in br:
                better = match.part2
                if match.part1.seed < match.part2.seed:
                    better = match.part1
                match.setwinner(better)
                c0 = (match.wlink)
                c1 = match.wlink not in nbr
                if c0 and (not match.wlink.isspecial()) and c1:
                    nbr.append(match.wlink)
            br = nbr


def loserGets(brackets, match):
    placing = len(brackets[0])*2 + 1
    shadowRealm = brackets[-1].copy()
    while match.llink is not None:
        match = match.llink
    if containsBye(match):
        match = match.wlink
    # print("SB:", match)

    matchlst = []
    round_index = 0
    while match not in matchlst:
        placing -= len(matchlst)
        round_index += 1
        matchlst = getmatchinrd(shadowRealm, round_index)
        # print(placing, matchlst)
    placing -= len(matchlst)
    round_index += 1
    matchlst = getmatchinrd(shadowRealm, round_index)
    # print(placing, matchlst)
    
    return placing


def minPlacing(brackets, participants):
    '''
    given a bracket and list of participants, returns a dict mapping Participant -> minimum placing
    '''
    place = OrderedDict()
    lst = []
    for participant in participants:
        sets = []

        for br_index in range(len(brackets)):
            for match in brackets[br_index]:
                if (match.part1 and match.part1.tag == participant) or (match.part2 and match.part2.tag == participant):
                    # print(f"{participant}: {match}")
                    if match not in sets:
                        sets.append(match)
        matchToAnalyze = sets[-1]
        while matchToAnalyze.winner == 1 and matchToAnalyze.part1 and matchToAnalyze.part1.tag == participant:
            matchToAnalyze = matchToAnalyze.wlink
        while matchToAnalyze.winner == 2 and matchToAnalyze.part2 and matchToAnalyze.part2.tag == participant:
            matchToAnalyze = matchToAnalyze.wlink
        
        # print(matchToAnalyze)
        lst.append([loserGets(brackets, matchToAnalyze), participant])
    lst.sort()
    return lst
        

def placing(brackets):
    '''
    given a bracket, returns a dict mapping Participant -> placing
    '''
    place = OrderedDict()
    placing = len(brackets[0])*2 + 1
    last = brackets[-1]
    rd = last
    nrd = []
    while(rd != []):
        placing = placing - len(rd)
        for m in rd:

            l = m.loser()
            if(l is not None):
                place[l] = placing
                place.move_to_end(l, False)
                if m.wlink is None:
                    place[m.winner_()] = 1
                    place.move_to_end(m.winner_(), False)

            if m.wlink not in nrd and m.wlink is not None:
                nrd.append(m.wlink)
        rd = nrd
        nrd = []
    return place


def getmatchinrd(bracket, rd, nummatches = -1):
    '''
    given a round, returns the matches in it
    '''
    returner = []
    retset = set()
    for m in bracket:
        mtch = m.itwlink(rd-1)
        if mtch is not None and mtch.uniqueid not in retset:
            retset.add(mtch.uniqueid)
            returner.append(mtch)
    if nummatches > 0:
        return returner[:nummatches]
    else:
        return returner

        
