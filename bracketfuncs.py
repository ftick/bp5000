# Bracket Functions, utilities for manipulating brackets.
#
#

from collections import OrderedDict


def shouldSkip(match, part):
    # print(match, part)
    if match is None:
        return False
    if match.wlink is None:
        return False
    if match.part1 is None and match.part2 is None:
        return False
    cond2 = (match.part2 is not None and match.part2.tag != part)
    cond3 = (match.part1 is not None and match.part1.tag != part)
    return cond2 and cond3


def formatPlacing(placeInt):
    onesDigit = placeInt % 10
    suffix = "th"
    if onesDigit == 1:
        suffix = "st"
    elif onesDigit == 2:
        suffix = "nd"
    elif onesDigit == 3:
        suffix = "rd"
    return f"{placeInt}{suffix}"


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


def loserGets(brackets, match, part=None):
    placing = len(brackets[0])*2 + 1
    shadowRealm = brackets[-1].copy()
    while match.llink is not None:
        match = match.llink
    if match.containsBye():
        match = match.wlink
    while shouldSkip(match, part):
        match = match.wlink
    while match.wonBy(part) and match.wlink is not None:
        match = match.wlink

    # print("SB:", match)
    # print("SB->", match.wlink)
    # if match.wlink is not None: print("SB->", match.wlink.wlink)
    
    # if match not in shadowRealm:
    if match.wlink is None: # Grand Finalist
        placing = 2
    elif match.wlink.wlink is None:
        if match.wonBy(part):
            placing = 2
            if match.wlink.wonBy(part):
                placing = 1
        else:
            placing = 3
    # elif match in shadowRealm and match.wlink is not None and match.wlink in shadowRealm:
    #     if match.wonBy(part):
    else:
        matchlst = []
        round_index = 0
        while match not in matchlst:
            placing -= len(matchlst)
            round_index += 1
            matchlst = getmatchinrd(shadowRealm, round_index)
            # print(placing, matchlst)
        placing -= len(matchlst)

    print(f"{formatPlacing(placing)}: {part}")
    return placing


def minPlacing(brackets, participants):
    '''
    given a bracket and list of participants, returns a dict mapping Participant -> minimum placing
    '''
    place = OrderedDict()
    lst = []
    for participant in participants:
        sets = []
        # print(f"{participant} placed...")

        for br_index in range(len(brackets)):
            for match in brackets[br_index]:
                if (match.part1 and match.part1.tag == participant) or (match.part2 and match.part2.tag == participant):
                    if match not in sets:
                        sets.append(match)
        matchToAnalyze = sets[-1]
        while matchToAnalyze is not None and matchToAnalyze.wonBy(participant):
            matchToAnalyze = matchToAnalyze.wlink

        # print(f"SB {participant}: {matchToAnalyze}")
        if matchToAnalyze is None:
            # print(f"1st: {participant}")
            lst.append([1, participant])
        else:
            # print(f"MA: {matchToAnalyze}")
            lst.append([loserGets(brackets, matchToAnalyze, participant), participant])

    # print(lst)
    lst.sort()
    return lst
        

def placing(brackets):
    '''
    (deprecated) given a bracket, returns a dict mapping Participant -> placing
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
    # print(rd)
    for m in bracket:
        mtch = m.itwlink(rd-1)
        if mtch is not None and mtch.uniqueid not in retset:
            retset.add(mtch.uniqueid)
            returner.append(mtch)
    if nummatches > 0:
        return returner[:nummatches]
    else:
        return returner

        
