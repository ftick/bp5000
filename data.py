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
        if (self.part1 == None):
            self.part1 = part
        elif self.part2 == None:
            self.part2 = part
        else:
            print("match has 2 participants")
    def setwinner(self, part):
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
            self.wlink.addpart(part)
        if(self.llink):
            self.llink.addpart(loser)
        else:
            #TODO: assign loser a placing.
            pass
        
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
        if player == None:
            pl.append(Participant(seed=sn))
        else:
            pl.append(Participant(tag=player,seed=sn))
            
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
            r  = int(r/2)
        print("r:" +str(r))
        seeda = matches[it-1-r].part1.seed
        wantseed = int(i/(r*2)) - seeda
        matches[it-1].part1 = pl[wantseed]
        matches[it-1].part2 = pl[-wantseed-1]
    '''
    for r in range(0, len(matches)):
        try:
            p = Participant(tag=players[r*2],seed=r*2+1)
            matches[r].addpart(p)
        except IndexError:
            bye = Participant(seed=(r*2 +1)) 
            matches[r].addpart(bye)
        try:
            p = Participant(tag=players[r*2+1],seed=r*2+2)
            matches[r].addpart(p)
        except IndexError:
            bye = Participant(seed=(r*2+2))
            matches[r].addpart(bye)
    '''
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
    while(len(cwb) == len(cwbo)):
        if(cwb != []):
            cwbo = cwb
            cwb = []
        for i in range(0, int(len(cwbo)/2)):
            n = Match("L")
            cwbo[i*2].llink = n
            cwbo[i*2+1].llink = n
            lblist.append(n)
        # add all unique winners of cwbo to cwb
        for r in range(0, len(cwbo)):
            if not (cwbo[r].wlink in cwb):
                cwb.append(cwbo[r].wlink)


    cwb = []
    for r in range(0, len(matches)):
        if matches[r].wlink in cwb:
            pass
        else:
            cwb.append(matches[r].wlink)
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




