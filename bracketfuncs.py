# Bracket Functions, utilities for manipulating brackets.
#
#


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
                cond0 = match.wlink.isspecial()
                if (match.wlink) and (not cond0) and (match.wlink not in nbr):
                    nbr.append(match.wlink)
            br = nbr


def placing(brackets):
    '''
    given a bracket, returns a dict mapping Participant -> placing
    '''
    place = {}
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

            if m.wlink not in nrd and m.wlink is not None:
                nrd.append(m.wlink)
        rd = nrd
        nrd = []
    return place
