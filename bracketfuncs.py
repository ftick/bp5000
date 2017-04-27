## Bracket Functions, utilities for manipulating brackets.
##
##

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
                better = match.part1 if match.part1.seed < match.part2.seed else match.part2
                match.setwinner(better)
                print(match.part1, match.part2)
                if (match.wlink) and (not match.wlink.isspecial()) and (not match.wlink in nbr):
                    nbr.append(match.wlink)
            br = nbr
