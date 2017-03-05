from PIL import Image, ImageDraw, ImageFont

def drawmatch(match):
    str1 = match.part1.tag if match.part1 else "TBD"
    int1 = match.part1.seed if match.part1 else ""
    str2 = match.part2.tag if match.part2 else "TBD"
    int2 = match.part2.seed if match.part2 else ""
    img = Image.new('RGBA',(200,80),color=(155,155,255))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf",20)
    d.font = font
    d.text((20,10), str(int1))
    d.text((60,10), str1)
    d.text((20,40), str(int2))
    d.text((60,40), str2)
    return img


def drawbracket(bracket):
    br = bracket
    img = Image.new('RGBA',(800, len(br)*120),color=(0,0,0))
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
        ymult = ymult*2
        br = nb
    return img


if __name__ == '__main__':
    import data
    b = data.genm(['player1','player2','player3','player4','player5','player6','player7','player8'])
    img = drawbracket(b)
    img.show()

