# grf.py - Graphical code
#
#
from PIL import Image, ImageDraw, ImageFont
import math

def drawmatch(match, highlight = False):
    str1 = match.part1.tag if match.part1 else "TBD"
    int1 = match.part1.seed if match.part1 else ""
    str2 = match.part2.tag if match.part2 else "TBD"
    int2 = match.part2.seed if match.part2 else ""
    img = Image.new('RGBA',(200,80),color=((155,155,255) if not highlight else (255, 155, 155)))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf",20)
    d.font = font
    d.rectangle((0,0,45,80), fill=(0,0,200))
    d.text((5,2), str(int1))
    d.text((60,2), str1)
    if match.winner != 0: 
        d.text((180,53 if match.winner == 2 else 2), u'\u2714', fill = (30,150,30))
    d.text((5,53), str(int2))
    d.text((60,53), str2)
    d.rectangle((0, 28, 200, 48), fill=(200,0,0))
    wt = (" W:"+match.wlink.getmatchdisp() if match.wlink else "")
    lt = (" L:"+match.llink.getmatchdisp() if match.llink else "")
    font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf",18)
    d.font = font
    d.text((0, 28), match.getmatchdisp()+wt+lt)
    return img

def drawspmatch(match):
    str1 = match.part1.tag if match.part1 else "TBD"
    int1 = match.part1.seed if match.part1 else ""
    str2 = match.part2.tag if match.part2 else "TBD"
    int2 = match.part2.seed if match.part2 else ""
    img = Image.new('RGBA',(200,80),color=(155,155,255))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf",20)
    d.font = font
    d.rectangle((0,0,45,80), fill=(0,0,200))
    d.text((5,2), str(int1))
    d.text((60,2), str1)
    d.text((180,2), str(match.upperleft), fill = (0,170,0))    
    d.text((5,53), str(int2))
    d.text((60,53), str2)
    d.text((180, 53), str(match.lowerleft), fill = (0,170,0))
    d.rectangle((0, 28, 200, 48), fill=(200,0,0))
    wt = (" W:"+match.wlink.getmatchdisp() if match.wlink else "")
    lt = (" L:"+match.llink.getmatchdisp() if match.llink else "")
    font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf",18)
    d.font = font
    d.text((0, 28), match.getmatchdisp()+wt+lt)
    return img

def mouse_ev(xm, ym, bracket, retm = False):
    br = bracket
    x = 30
    ymult = 1
    while(br[0] is not None):
        nb = []
        y = 30 + (ymult-1)*60
        for ma in br:
            rect = (x, y, 200, 80)
            #print((xm, ym), rect)
            if intersect((xm,ym),rect) and (not ma.isspecial()):
                return ma if retm else (drawmatch(ma, True), x, y)
            y += 120*ymult
            if not (ma.wlink in nb):
                nb.append(ma.wlink)
        x += 220
        ymult = ymult*int(len(br)/len(nb))
        br = nb
    return None

def intersect(pt, rect):
    return (rect[0] <= pt[0] <= rect[0]+rect[2]) and (rect[1] <= pt[1] <= rect[1]+rect[3])
def drawbracket(bracket):
    br = bracket
    tm = br[0]
    rounds = 0
    while(not tm.wlink is None and not tm.wlink.isspecial()):
        tm = tm.wlink
        rounds += 1
    img = Image.new('RGBA',(250+int(220*rounds), len(br)*120),color=(0,0,0))
    x = 30
    ymult = 1
    while(br[0] is not None):
        nb = []
        y = 30 + (ymult-1)*60
        for ma in br:
            im = drawmatch(ma)
            img.paste(im, (x, y))
            y += 120*ymult
            if not (ma.wlink in nb):
                nb.append(ma.wlink)
        x += 220
        ymult = ymult*int(len(br)/len(nb))
        br = nb
    return img

def firstgf(match):
    m = match
    while not m.isspecial():
        m = m.wlink
    return m

def drawfinals(brackets):
    gfs = [firstgf(brackets[r][0]) for r in range(len(brackets)-2,-1, -1)]
    img = Image.new('RGBA',(30+(len(gfs)*250), 120),color=(0,0,0))
    xpos = 20
    for gf in gfs:
        im = drawspmatch(gf)
        img.paste(im, (xpos, 20))
        xpos += 220
    return img

if __name__ == '__main__':
    import data
    i = 32
    plist = (['player %s ' % x for x in range(0,i)])
    b = data.genm(plist)
    l = data.genl(b)
    l2 = data.genl(l)
    data.fbracket([b,l,l2])
    import bracketfuncs
    bracketfuncs.projected([b, l, l2])
    img = drawbracket(b)
    im2g = drawbracket(l)
    im3g = drawbracket(l2)
    imfg = drawfinals([b,l,l2])
    img.save("winners.png")
    im2g.save("losers.png")
    im3g.save("losers2x.png")
    imfg.save("finals.png")

