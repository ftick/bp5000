# grf.py - Graphical code
#
#
from PIL import Image, ImageDraw, ImageFont
import bracketfuncs

# Colour of the lines
lcolor = (255, 195, 155)
FONTPATH = ["verdana.ttf", "Helvetica.dfont",
            "Helvetica.ttf", "DejaVuSans.ttf"]


# mathematical functions for bracket positioning
def fx(r):
    return (220*r)-190

def fx_inv(x):
    return (x+190.0)/220.0

def fy(m, r):
    return 30*(2**r)+60*(2**r)*(m-1)-30

def fy_inv(y, r):
    return (((y+30)-(30*(2**r)))/(60*(2**r)))+1

def getFont(sz, num=0):
   # import pdb; pdb.set_trace()
    try:
        fnt = ImageFont.truetype(FONTPATH[num], sz)
        return fnt
    except OSError:
        try:
            return getFont(sz, num+1)
        except:
            s = "FATAL: no fonts found. install"
            s2 = " DejaVuSans, verdana or Helvetica"
            print(s+s2)


ckb = None


def getchek():
    global ckb
    if ckb is None:
        data = (b'iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAYAAA'
                b'A71pVKAAABVUlEQVR4nGNgGJKAkRTF7ErsVlxGXCGMHIx8Xw5'
                b'9mU6cZkYGJoFAgS4+F75iBgYGht/Pf1992f3SioWgRiYGZpEE'
                b'kSVcJlwRDAwMDH8//X3xeupr738//n1iIqRXKFJoBkzj/9//v7'
                b'+e/trvz7s/DyHm4gG8TryFPNY8KQwMDAwM/xn+v13wNvbXw1+nE'
                b'Y6CMbiZhAX8BFqEYoTmMjAwMLArsVsKBgl2weQ/bP5Q++38t7XIh'
                b'sP9LBgs2MttwR3PwMDA8P3i9/WCYYKTGJgg8t/Oflv1acenVnSXw'
                b'TX/+/bvPYwtmim6Gcb+/ez35beL3yZi8xbc2T9u/ziILvnvx7/Pr2'
                b'e9Dv7/6/83/Jqv/dj578e/T8iS71e9z/3z6s9tbBpRNP///f/7l4Nf'
                b'psH43y993/j1xNeFuDQyMKAnT0YGJjY5NiOGfwz/fj35dYHhP8M/fJo'
                b'BGuqDl4b7We4AAAAASUVORK5CYII=')
        import base64
        from io import BytesIO
        ckb = Image.open(BytesIO(base64.b64decode(data)))
    return ckb


def drawmatch(match, highlight=False):
    if match.containsBye():
        return Image.new('RGBA', (200, 80), color=((0, 0, 0)))
    if match.isspecial():
        return drawspmatch(match, highlight)
    str1 = match.part1.tag if match.part1 else "TBD"
    int1 = match.part1.seed if match.part1 else ""
    str2 = match.part2.tag if match.part2 else "TBD"
    int2 = match.part2.seed if match.part2 else ""
    img = Image.new('RGBA', (200, 80),
                    color=((155, 155, 255) if not highlight else (255,
                                                                  155, 155)))
    d = ImageDraw.Draw(img)
    font = getFont(20)
    d.font = font
    d.rectangle((0, 0, 45, 80), fill=(0, 0, 200))
    d.text((5, 2), str(int1))
    d.text((60, 2), str1)
    if str1 != "TBD" and str2 != "TBD":
        #img.paste(getchek(), (180, 56 if match.winner == 2 else 5), getchek())
        d.text((180, 2), str(match.p1score), fill=((0,120,0) if match.winner==1 else (0,0,0)))
        d.text((180, 53), str(match.p2score), fill=((0,120,0) if match.winner==2 else (0,0,0)))
    d.text((5, 53), str(int2))
    d.text((60, 53), str2)
    d.rectangle((0, 28, 200, 48), fill=(200, 0, 0))
    wt = (" W:"+match.wlink.getmatchdisp() if match.wlink else "")
    lt = (" L:"+match.llink.getmatchdisp() if match.llink else "")
    font = getFont(18)
    d.font = font
    d.text((0, 28), match.getmatchdisp()+wt+lt)
    return img


def drawspmatch(match, highlight=False):
    str1 = match.part1.tag if match.part1 else "TBD"
    int1 = match.part1.seed if match.part1 else ""
    str2 = match.part2.tag if match.part2 else "TBD"
    int2 = match.part2.seed if match.part2 else ""
    img = Image.new('RGBA', (200, 80),
                    color=((155, 155, 255) if not highlight else (255,
                                                                  155, 155)))
    d = ImageDraw.Draw(img)
    font = getFont(20)
    d.font = font
    d.rectangle((0, 0, 45, 80), fill=(0, 0, 200))
    d.text((5, 2), str(int1))
    d.text((60, 2), str1)
    #d.text((180, 2), str(match.upperleft), fill=(0, 170, 0))
    d.text((5, 53), str(int2))
    d.text((60, 53), str2)
    #d.text((180, 53), str(match.lowerleft), fill=(0, 170, 0))
    x01 = 170
    for m in match.scores:
        #first = upper
        d.text((x01, 2), str(m[0]), fill = (0, 120, 0) if m[0] > m[1] else (0,0,0))
        d.text((x01, 53), str(m[1]), fill = (0, 120, 0) if m[1] > m[0] else (0,0,0))
        x01 += 20
    d.rectangle((0, 28, 200, 48), fill=(200, 0, 0))
    wt = (" W:"+match.wlink.getmatchdisp() if match.wlink else "")
    lt = (" L:"+match.llink.getmatchdisp() if match.llink else "")
    font = getFont(18)
    d.font = font
    d.text((0, 28), match.getmatchdisp()+wt+lt)
    return img


def mouse_ev(xm, ym, bracket, retm=False):
    if isinstance(bracket[0], list):
        return mouse_ev_finals(xm, ym, bracket, retm)
    br = bracket
    x = 30
    ymult = 1
    while(br[0] is not None):
        nb = []
        y = 30 + (ymult-1)*60
        for ma in br:
            rect = (x, y, 200, 80)
            if intersect((xm, ym), rect) and (not ma.isspecial()):
                return ma if retm else (drawmatch(ma, True), x, y)
            y += 120*ymult
            if not (ma.wlink in nb):
                nb.append(ma.wlink)
        x += 220
        ymult = ymult*int(len(br)/len(nb))
        br = nb
    return None


def mouse_ev_finals(xm, ym, brackets, retm):
    gfs = [firstgf(brackets[r][0]) for r in range(len(brackets)-2, -1, -1)]
    xpos = 20
    for gf in gfs:
        rect = (xpos, 20, 200, 80)
        if intersect((xm, ym), rect):
            return gf if retm else (drawspmatch(gf, True), xpos, 20)
        xpos += 220
    return None


def intersect(pt, rect):
    cond1 = (rect[0] <= pt[0] <= rect[0]+rect[2])
    cond2 = (rect[1] <= pt[1] <= rect[1]+rect[3])
    return cond1 and cond2


def drawbracketFAST(bracket, viewport):
    '''
    FAST bracket drawing.
    should not vary with bracket size
    draws over million matches in less than quarter second
    '''
    import time
    tm = time.time()
    vx = viewport[0]
    vy = viewport[1]
    vw = viewport[2]
    vh = viewport[3]
    img = Image.new('RGBA', (vw, vh), color=(0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # the pan num for x, y, for laying out the match.
    # we calculate the matches that should display at a specific location.
    # starting round.
    startrd = 1 # include rounds starting at 1
    var = 220
    while var < vx:
        # if we can skip a rd and are still offscreen, test the next round.
        startrd += 1
        var += 220
    # Grab all matches for the starting round.
    mx = var
    matches = bracketfuncs.getmatchinrd(bracket, startrd)
    # determine u/d for match.
    m50s = matches
    
    while len(m50s) > 0:
        nm50s = []
        dire = False # 'dire'ction
        for m50 in m50s:
            m50.up = dire
            dire = not dire
            if m50.wlink is not None and m50.wlink not in nm50s and (not m50.wlink.isspecial()):
               nm50s.append(m50.wlink)
        m50s = nm50s
        
        
    # could draw all these matches + children. while an improvement,  this is still too slow.
    # figure out y for first match.
    # y = 0
    spacing = 120 # 120 y px between each match
    fm = bracket[0]
    curmy = 0
    first = True
    while fm != matches[0].wlink:
        if (not fm.loserlinked) and (not first):
            curmy = (curmy + spacing) / 2
            spacing = spacing * 2
        first = False
        fm = fm.wlink
    # now curmy = ypos of first match
    # delta = current match y - first match y * 2
    # so nth match y = fmmatchinrdy + delta(n-1)
    delta = spacing
    startmatch = 0
    var = curmy
    while var < vy:
        startmatch += 1
        var += delta
    my = var
        
    #
    # have first match now
    # 
    
    # (pos to put match) = abs pos of match - viewport pos
    #
    #
    
    matches = matches[startmatch:]
    mdrawnid = set()
    print(" -- -- - - ")
    print("Starting @ "+ repr((mx, my)))
    print("delta: "+str(delta)+", curmy+ "+str(curmy))
    print(" -- - -- - ")
    for m in matches:
        match = m
        # if not match.containsBye():
        img.paste(drawmatch(match), (int(mx - vx), int(my - vy)))
        mdrawnid.add(match.uniqueid)
        print("first: draw "+ str(match.up)+" "+ str(match)+ " @ "+ repr((int(mx - vx), int(my - vy))))
        print("")
        lastchain = False
        if my - vy > vw:
            lastchain = True
        mx_old = mx
        my_old = my
        fakedelta = delta
        while match.wlink is not None and (not match.wlink.isspecial()):
            oldm = match
            match = match.wlink
            mx += 220
            if not match.loserlinked:
                if oldm.up:
                    my = (my + my - fakedelta) / 2
                else:
                    my = (my + my + fakedelta) / 2
                fakedelta = fakedelta * 2
            if mx - vx > vw:
                break
            if match.uniqueid not in mdrawnid:
                # if not match.containsBye():
                img.paste(drawmatch(match), (int(mx - vx), int(my - vy)))
                print("draw "+ str(match.up)+" "+str(match)+ " @ "+ repr((int(mx - vx), int(my - vy))))
                mdrawnid.add(match.uniqueid)
        if lastchain:
            break
        mx = mx_old
        my = my_old + delta
    return img
    
'''    
    rds = math.floor(fx_inv(x))
    rdmax = math.ceil(fx_inv(x+w))
    if rds < 1:
        rds = 1
    # matches to skip to get to viewport
    matches = math.floor(fy_inv(y, rds))
    # last match #
    matches_max = math.ceil(fy_inv(y+h, rds))
    sav0 = bracketfuncs.getmatchinrd(bracket, rds)
    fm = bracket[0]
    fakerds = 0
    xboost = 0
    a = True
    while fm != sav0[0]:
        print(fm)
        if fm.loserlinked:
            fakerds += 1
            xboost += 220
        #rds -= 1
        #x -= 220
        ## loserlink first round regardless
        if a and bracket[0].wlink != bracket[1].wlink:
            fakerds += 1
            xboost += 220
            a = False
        fm = fm.wlink
    print("Fakes: "+str(fakerds))
    rds = rds - fakerds
    mtchs = sav0[matches:matches_max]
    xpos = fx(rds)
    newmtch = []
    bar = False
    
    while fx(rds)-x <= fx(rdmax)-viewport[0]:
        mn = matches+1
        for mtch in mtchs:
            print(str(mtch)+" RDNUM: "+str(rds)+ " mn: "+str(mn)+ " x: "+str(x)+ " y: "+str(y) + " xboost: "+str(xboost))
            im = drawmatch(mtch)
            #print("rds: "+str(rds)+" mn: "+str(mn))
            #print("("+str(fx(rds)-x)+", "+str(fy(mn, rds)-y))
            
            if mtch.wlink is not None and not mtch.wlink.isspecial():
                
                d.rectangle((fx(rds)-x+200 + xboost, fy(mn, rds)-y+36, fx(rds)-x+320+xboost, fy(mn, rds)-y+40), fill=lcolor)
            if not mtch.loserlinked:
                d.rectangle((fx(rds)-x+100 + xboost, fy(mn*2 -1, rds-1)-y+36, fx(rds)-x+104+xboost, fy(mn*2, rds-1)-y+40), fill=lcolor)
            img.paste(im, (fx(rds)-x+xboost, fy(mn, rds)-y))
            mn += 1
            if mtch.wlink is not None and not mtch.wlink.isspecial() and mtch.wlink not in newmtch:
                newmtch.append(mtch.wlink)
        bar = not mtchs[0].loserlinked
        if len(newmtch) == 0:
            break
        if newmtch[0].loserlinked:
            rds -= 1
            xboost += 220
            pass
            #print("loserrd")
      #  elif newmtch[0].wlink and newmtch[0].wlink.isspecial:
        ##      xboost += 220
        else:
            matches = math.floor(matches/2)
        mtchs = newmtch
        newmtch = []
        rds += 1
    #print("-----------")
    #print(str(time.time()-tm))
    #print("-----------")
    return img
'''    
def drawbracket(bracket):
    br = bracket
    tm = br[0]
    rounds = 0
    while(tm.wlink is not None and not tm.wlink.isspecial()):
        tm = tm.wlink
        rounds += 1
    img = Image.new('RGBA', (250+int(220*rounds),
                             len(br)*120), color=(0, 0, 0))
    d = ImageDraw.Draw(img)
    x = 30
    ymult = 1
    rdc = len(br)
    dbar = False
    while(br[0] is not None):
        dbar = (rdc != len(br))
        nb = []
        y = 30 + (ymult-1)*60
        fakey = (30+(((ymult/2)-1)*60))
        for ma in br:
            # if not match.containsBye():
            im = drawmatch(ma)
            if(dbar):
                # y mult /2
                ny = fakey + (120*ymult/2)
                d.rectangle((x+100, fakey+36, x+104, ny+40), fill=lcolor)
                fakey = ny + (120*ymult/2)

            img.paste(im, (x, y))
            #print("("+str(x)+", "+str(y)+")")
            if ma.wlink is not None and not ma.wlink.isspecial():
                d.rectangle((x+200, y+36, x+320, y+40), fill=lcolor)
            if not (ma.wlink in nb):
                nb.append(ma.wlink)
            y += 120*ymult
        
        x += 220
        ymult = ymult*int(len(br) / len(nb))
        rdc = len(br)
        br = nb
    return img


def firstgf(match):
    m = match
    while not m.isspecial():
        m = m.wlink
    return m


def drawfinals(brackets):
    gfs = [firstgf(brackets[r][0]) for r in range(len(brackets)-2, -1, -1)]
    img = Image.new('RGBA', (30+(len(gfs)*250), 120), color=(0, 0, 0))
    xpos = 20
    for gf in gfs:
        im = drawspmatch(gf)
        img.paste(im, (xpos, 20))
        xpos += 220
    return img

if __name__ == '__main__':
    import data
    i = 64
    plist = (['player %s ' % x for x in range(0, i)])
    b = data.genm(plist)
    l = data.genl(b)
    #l2 = data.genl(l)
    #data.fbracket([b, l, l2])
    #import bracketfuncs
    #bracketfuncs.projected([b, l, l2])
    #print(fy(i, 1))
    img = drawbracketFAST(b, (0, 0, 2000, 1000))
    im2g = drawbracketFAST(b, (500, 100, 900, 500))
    #im3g = drawbracket(l2)
    #imfg = drawfinals([b, l, l2])
    im2g.show()


"""
from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGBA', (15, 15))
draw = ImageDraw.Draw(img)
draw.font = ImageFont.truetype("DejaVuSans.ttf", 20)
draw.text((0, -3), u'\u2714', fill=(30, 150, 30))
## convert to base64

b'iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAYAAAA71pVKAAABVUlEQVR4nGNgGJKAkRTF7ErsVlxGXCGMHIx8Xw59mU6cZkYGJoFAgS4+F75iBgYGht/Pf1992f3SioWgRiYGZpEEkSVcJlwRDAwMDH8//X3xeupr738//n1iIqRXKFJoBkzj/9//v7+e/trvz7s/DyHm4gG8TryFPNY8KQwMDAwM/xn+v13wNvbXw1+nEY6CMbiZhAX8BFqEYoTmMjAwMLArsVsKBgl2weQ/bP5Q++38t7XIhsP9LBgs2MttwR3PwMDA8P3i9/WCYYKTGJgg8t/Oflv1acenVnSXwTX/+/bvPYwtmim6Gcb+/ez35beL3yZi8xbc2T9u/ziILvnvx7/Pr2e9Dv7/6/83/Jqv/dj578e/T8iS71e9z/3z6s9tbBpRNP///f/7l4NfpsH43y993/j1xNeFuDQyMKAnT0YGJjY5NiOGfwz/fj35dYHhP8M/fJoBGuqDl4b7We4AAAAASUVORK5CYII='
"""
