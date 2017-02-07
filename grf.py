from PIL import Image, ImageDraw, ImageFont

def drawmatch(match):
    str1 = match.part1.tag
    int1 = match.part1.seed
    str2 = match.part2.tag
    int2 = match.part2.seed
    img = Image.new('RGBA',(200,80),color=(155,155,255))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf",20)
    d.font = font
    d.text((20,10), str(int1))
    d.text((60,10), str1)
    d.text((20,40), str(int2))
    d.text((60,40), str2)
    return img

import pdb; pdb.set_trace()
if __name__ == '__main__':
    import data
    b = data.genm(['bob','joe','STEVE','kevin'])
    img = drawmatch(b[0])
    img.show()
