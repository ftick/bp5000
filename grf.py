from PIL import Image, ImageDraw, ImageFont
import math

def drawmatch(match):
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
    d.text((5,53), str(int2))
    d.text((60,53), str2)
    d.rectangle((0, 28, 200, 48), fill=(200,0,0))
    wt = (" W:"+match.wlink.getmatchdisp() if match.wlink else "")
    lt = (" L:"+match.llink.getmatchdisp() if match.llink else "")
    font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf",18)
    d.font = font
    d.text((0, 28), match.getmatchdisp()+wt+lt)
    return img


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
        print(br)
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


if __name__ == '__main__':
    import data
    i = 32
    plist = (['player %s ' % x for x in range(0,i)])
    b = data.genm(plist)
    l = data.genl(b)
    l2 = data.genl(l)
    import bracketfuncs
    bracketfuncs.projected([b, l, l2])
    img = drawbracket(b)
    im2g = drawbracket(l)
    im3g = drawbracket(l2)
    im2g.show()
    im3g.show()

