import struct

# used for file version compatibility
VERSION_CODE = 1


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

#
# Matches:
# 4 : match code
# 1 : has wlink
# 4 : wlink code
# 1 : has llink
#
def match_w(match):
    '''
    returns bytes represting the match, that can be decoded by
    match_r
    '''
    mid = match.uniqueid
    haswl = match.wlink is not None
    hasll = match.llink is not None
    wcode = 0
    lcode = 0
    if haswl:
        wcode = match.wlink.uniqueid
    if hasll:
        lcode = match.llink.uniqueid
    
    return mid + haswl + wcode + hasll + lcode
