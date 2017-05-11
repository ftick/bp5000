import math


pid = 1
uid = 1


class Participant:

    def __init__(self, tag=None, seed=None):
        if tag:
            self.tag = tag
            global pid
            self.uniqueid = pid
            pid += 1
        else:
            self.tag = "Bye"
            self.uniqueid = 0
        self.seed = seed

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.seed)+": "+self.tag

    def isbye(self):
        return self.uniqueid == 0


class Match:

    def __init__(self, data=None):
        self.llink = None
        self.wlink = None
        self.data = data
        self.part1 = None
        self.part2 = None
        self.winner = 0
        global uid
        self.uniqueid = uid
        uid += 1

    def addpart(self, part):
        if (self.part1 is None):
            self.part1 = part
        elif self.part2 is None:
            if self.part1.isbye():
                self.part2 = part
                self.setwinner(self.part2)
                return
            if part.isbye():
                self.part2 = part
                self.setwinner(self.part1)
                return
            self.part2 = part
            if self.part2.seed < self.part1.seed:
                self.part2 = self.part1
                self.part1 = part

        else:
            print("match has 2 participants")

    def loser(self):
        if self.winner == 1:
            return self.part2
        if self.winner == 2:
            return self.part1

    def winner_(self):
        if self.winner == 2:
            return self.part2
        if self.winner == 1:
            return self.part1

    def setwinner(self, part):
        if (self.winner != 0):
            self.settbd()
        loser = None
        if(part == self.part1):
            self.winner = 1
            loser = self.part2
        elif (part == self.part2):
            self.winner = 2
            loser = self.part1
        else:
            print("error no winner")
            return
        if(self.wlink):
            if self.wlink.isspecial():
                self.wlink.addpart(part, self.upper)
            else:
                self.wlink.addpart(part)
        if(self.llink):
            self.llink.addpart(loser)
        else:
            # TODO: assign loser a placing.
            pass

    def settbd(self):
        w = self.part1 if self.winner == 1 else self.part2
        l = self.part1 if self.winner == 2 else self.part2
        self.winner = 0
        if self.wlink:
            self.wlink.settbd()
            if self.wlink.part1 == w:
                self.wlink.part1 = None
            elif self.wlink.part2 == w:
                self.wlink.part2 = None
        if self.llink:
            self.llink.settbd()
            if self.llink.part1 == l:
                self.llink.part1 = None
            elif self.llink.part2 == l:
                self.llink.part2 = None

    def u(self):
        return str(self.uniqueid)

    def __str__(self):
        p1t = self.part1.tag if self.part1 else '?'
        p2t = self.part2.tag if self.part2 else '?'
        rstr = p1t + ' vs ' + p2t
        return 'M'+str(self.uniqueid)+'('+rstr+')'

    def __eq__(self, other):
        return self.uniqueid == other.uniqueid

    def __repr__(self):
        return self.__str__()

    def itllink(self, num):
        if(num == 1):
            return self.llink
        return self.llink.itllink(num-1)

    def itwlink(self, num):
        if(num == 1):
            return self.wlink
        return self.wlink.itwlink(num-1)

    def getmatchdisp(self):
        return "M"+str(self.uniqueid)

    def isspecial(self):
        return False


#
# Steps to create a bracket:
# b = genm / gen to create initial
# then genl(b) to create losers brackets (repeat for more)
# then fbracket([w, l, 2l, 3l ...]) to finalize bracket
#
def create(plist, elim):
    #
    # entrants | elim
    #
    # 4 entants - 1-2
    # 8           3-4
    # 16          8
    # 32          16
    #
    #
    if len(plist) < 4 or len(plist) <= elim:
        return "Elimination # too high for # of players"
    brackets = [genm(plist)]
    for i in range(1, elim):
        brackets.append(genl(brackets[-1]))
    fbracket(brackets)
    progbyes(brackets[0])
    return brackets


def progbyes(br):
    for m in br:
        if m.part1.isbye():
            m.setwinner(m.part2)
        elif m.part2.isbye():
            m.setwinner(m.part1)


def genm(players):
    # Generates a winners bracket from a list
    # of players, ordered by seed

    i = 1
    while(i < len(players)):
        i = i*2
    while (len(players) < i):
        players.append(None)
    print(players)
    # now players should be a 2^n size bracket,
    # with byes filling up the rest. now transform tags -> participants
    pl = []
    sn = 0
    for player in players:
        sn += 1
        if player is None:
            pl.append(Participant(seed=sn))
        else:
            pl.append(Participant(tag=player, seed=sn))

    matches = gen(int(i/2))
    # i = identity. important.
    # for first round matches, seeds add up to i+1.
    # second rounds, i/2 + 1
    # 3rd, i/4 + 1 etc.
    matches[0].part1 = pl[0]
    matches[0].part2 = pl[-1]
    it = 1
    for m in matches[1:]:
        it += 1
        '''
        if(it % 2 == 0):
            seed2a = matches[it-2].part1.seed
            wantseed = int(i/2)-seed2a-1
            matches[it-1].part1 = players[wantseed-1]
            matches[it-1].part2 = players[-wantseed]
        '''
        r = 65536
        while((it-1) % r != 0):
            r = int(r/2)
        seeda = matches[it-1-r].part1.seed
        wantseed = int(i/(r*2)) - seeda
        matches[it-1].part1 = pl[wantseed]
        matches[it-1].part2 = pl[-wantseed-1]
    return matches


def gen(npart):
    mlist = []
    blist = []
    to = npart
    while(to > 1):
        for n in range(1, to+1):
            m = Match(n)
            if(to != npart):
                mlisto[n*2-2].wlink = m
                mlisto[n*2-1].wlink = m
            else:
                blist.append(m)
            mlist.append(m)
        to = int(to/2)
        mlisto = mlist
        mlist = []
    m = Match(1)
    mlisto[0].wlink = m
    mlisto[1].wlink = m
    return blist


def genl(matches):
    '''
    generates a losers bracket given a winners
    bracket.
    '''
    prev = None
    lblist = []
    cwb = matches
    cwbo = matches
    run = 0
    while(len(cwb) == len(cwbo)):
        run += 1
        if run == 3:
            break
        if(cwb != []):
            cwbo = cwb
            cwb = []
        for i in range(0, int(len(cwbo)/2)):
            n = Match("L")
            cwbo[i*2].llink = n
            cwbo[i*2+1].llink = n
            lblist.append(n)
        # add all unique winners of cwbo to cwb
        # (advance to next round)
        for r in range(0, len(cwbo)):
            if not (cwbo[r].wlink in cwb):
                cwb.append(cwbo[r].wlink)

    # new wb should be half size as old.
    # if it is the same, need to
    clb = lblist
    while(len(clb) > 1):
        # 2 cases. either winners bracket players
        # come into losers too play or losers bracket
        # players play each other
        nlb = []
        if(len(cwb) == len(clb)):
            print("both #"+str(len(cwb)))
            for r in range(0, len(cwb)):
                m = Match("L")
                cwb[r].llink = m
                clb[r].wlink = m
                nlb.append(m)
            nwb = []
            for r in range(0, len(cwb)):
                if not(cwb[r].wlink in nwb):
                    nwb.append(cwb[r].wlink)
            cwb = nwb

        else:
            print("lb#"+str(len(clb))+" wb#"+str(len(cwb)))
            for r in range(0, int(len(clb)/2)):
                m = Match("L")
                clb[r*2].wlink = m
                clb[r*2+1].wlink = m
                nlb.append(m)
        clb = nlb
    return lblist


def finalm(m):
    while not (None is m.wlink):
        m = m.wlink
    return m


class SpecialMatch(Match):
    ''' A Special match for grand final type sets
    where people play multiple times
    NOTE: upper player is p1, lower is p2
    '''

    def __init__(self, upperleft=None, lowerleft=None, data=None):
        self.llink = None
        self.wlink = None
        self.data = data
        self.upperleft = upperleft
        self.lowerleft = lowerleft
        self.part1 = None
        self.part2 = None
        self.winner = 0
        global uid
        self.uniqueid = uid
        uid += 1

    def addpart(self, part, upper):
        if (upper):
            self.part1 = part
        else:
            self.part2 = part

    def setwinner(self, part, setsleft):
        if self.wlink:
            self.wlink.addpart(part, False)
            self.wlink.lowerleft = setsleft
        if(part == self.part1):
            self.winner = 1
        elif (part == self.part2):
            self.winner = 2

    def settbd(self):
        if self.wlink:
            self.wlink.settbd()
            w = None
            if self.winner == 1:
                w = self.part1
            if self.winner == 2:
                w = self.part2
            if w:
                if self.wlink.part1 == w:
                    self.wlink.part1 = None
                if self.wlink.part2 == w:
                    self.wlink.part2 = None
        self.winner = 0
        self.upperleft = self.max_sets
        self.lowerleft = self.max_sets - 1

    def isspecial(self):
        return True


def fbracket(brackets):
    '''
    finalize bracket. this links brackets together
    (ie grand finals in a double elim bracket)
    '''
    # make finals of brackets
    for i in range(len(brackets), 0, -1):
        for r in range(i, len(brackets)):
            f2b(brackets[r-1], brackets[r])

    # make gfs, matches that break the laws of multi elim format
    for r in range(0, len(brackets)-1):
        b = len(brackets) - r - 1
        gf = SpecialMatch(r+2, r+1, "G")
        lower = finalm(brackets[b][0])
        upper = finalm(brackets[b-1][0])
        lower.wlink = gf
        upper.wlink = gf
        upper.upper = True
        lower.upper = False
        gf.max_sets = r+2


def f2b(b1, b2):
    nmatch = Match("F")
    finalm(b1[0]).llink = nmatch
    finalm(b2[0]).wlink = nmatch
