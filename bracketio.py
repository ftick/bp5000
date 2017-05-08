import struct

# used for file version compatibility
VERSION_CODE = 1


def write_bracket(fil, br):
    s = open(fil, 'wb')
    s.write(entire_w(br))
    s.close()


def int_w(nt):
    return struct.pack(">I", nt)


def int_r(bn):
    return struct.unpack(">I", bn)


def bool_w(bol):
    val = 0
    if bol:
        val = 1
    return bytes([val])


def bool_r(bn):
    return (bn == bytes([1]))


def entire_w(brs):
    bts = int_w(VERSION_CODE)
    for br in brs:
        bts = bts + bracket_w(br)
    return bts


def bracket_w(br):
    nbr = []
    bts = None
    while len(br) != 0:
        for m in br:
            if bts is None:
                bts = match_w(m)
            else:
                bts = bts + match_w(m)
            if m.wlink is not None and m.wlink not in nbr:
                nbr.append(m.wlink)
        br = nbr
        nbr = []

    return bts


#
# Matches:
# 4 : match code
# 1 : has wlink
# 4 : wlink code
# 1 : has llink
# 4 : llink code
# 1 : has part1
# 4 : part1 code
# 1 : has part2
# 4 : part2 code
# 4 : wincode
#
# 28 bytes
#
def match_w(match):
    '''
    returns bytes represting the match, that can be decoded by
    match_r
    '''
    mid = match.uniqueid
    haswl = bool_w(match.wlink is not None)
    hasll = bool_w(match.llink is not None)
    wcode = int_w(0)
    lcode = int_w(0)
    if match.wlink is not None:
        wcode = int_w(match.wlink.uniqueid)
    if match.llink is not None:
        lcode = int_w(match.llink.uniqueid)

    hasp1 = bool_w(match.part1 is not None)
    hasp2 = bool_w(match.part2 is not None)
    p1code = int_w(0)
    p2code = int_w(0)
    if match.part1 is not None:
        p1code = int_w(match.part1.uniqueid)
    if match.part1 is not None:
        p2code = int_w(match.part2.uniqueid)

    wincode = int_w(match.winner)

    mp32 = mid + haswl + wcode + hasll + lcode + hasp1
    return mp32 + p1code + hasp2 + p2code + wincode
