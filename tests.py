from unittest import TestCase
import unittest
import data
import bracketfuncs
import bracketio
import importplayers


class test_brackets(TestCase):

    def test1de(self):
        w = data.gen(16)
        l = data.genl(w)
        m = w[0].llink.wlink.wlink.wlink.wlink.wlink.wlink
        for r in range(1, 16):
            self.assertEqual(m, w[r].llink.wlink.wlink.wlink.wlink.wlink.wlink)
        self.assertEqual(m, w[15].wlink.wlink.wlink.llink.wlink)

    def test2genm(self):
        w = data.genm(['a', 'b', 'c', 'd'])
        self.assertEqual(w[0].part1.tag, 'a')
        self.assertEqual(w[0].part2.tag, 'd')
        self.assertEqual(w[1].part1.tag, 'b')
        self.assertEqual(w[1].part2.tag, 'c')

    def test3place(self):
        w = data.genm(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
        l = data.genl(w)
        data.fbracket([w, l])
        bracketfuncs.projected([w, l])
        placingex = {'h': 7, 'g': 7, 'f': 5, 'e': 5, 'd': 4, 'c': 3}
        pl = bracketfuncs.placing([w, l])
        for p in pl:
            self.assertEqual(placingex[p.tag], pl[p])


class test_iobrackets(TestCase):

    def test1writeread(self):
        i = 128
        plist = (['player %s ' % x for x in range(0, i)])
        b = data.genm(plist)
        l = data.genl(b)
        l2 = data.genl(l)
        l3 = data.genl(l2)
        l4 = data.genl(l3)
        bracketio.write_bracket("TEST_FILE.bp5", [b, l, l2, l3, l4])
        r = bracketio.read_bracket("TEST_FILE.bp5")
        self.assertEqual(repr([b, l, l2, l3, l4]), repr(r))


class test_importplayers(TestCase):
    def test1url_challongeshort(self):
        url = 'https://challonge.com/mmrscmbr'
        actual = importplayers.url_challonge(url)
        self.assertEqual(repr(["","mmrscmbr"]), repr(actual))

    def test2url_challongeorg(self):
        url = 'https://uwsmashclub.challonge.com/uwu40'
        actual = importplayers.url_challonge(url)
        self.assertEqual(repr(["uwsmashclub","uwu40"]), repr(actual))

    def test3url_startgg1(self):
        url = 'https://start.gg/tournament/the-function-brooklan/event/melee-singles'
        actual = importplayers.url_startgg(url)
        self.assertEqual(repr(["the-function-brooklan","melee-singles"]), repr(actual))

    def test4url_smashgg1(self):
        url = 'https://smash.gg/tournament/the-function-brooklan/event/melee-singles'
        actual = importplayers.url_startgg(url)
        self.assertEqual(repr(["the-function-brooklan","melee-singles"]), repr(actual))

    def test5entrants_challongeurl(self):
        url = 'https://challonge.com/mmrscmbr'
        actual = importplayers.entrants_challongeurl(url)
        self.assertEqual(repr(['Errrg', 'LiteralFraud', 'Dope', 'MidnightBlue', 'Hello', 'The Clencher', 'Xxstdyk', 'Extenderrrrrr', 'Stealthhack', 'Leor', 'Fade', 'Sawah', 'Hundereds', 'Chiromite', 'Maebell', 'Withered', 'Xplr']), repr(actual))

    def test6entrants_startggurl(self):
        url = 'https://www.start.gg/tournament/melee-verdugo-west-145/event/melee-singles'
        actual = importplayers.entrants_startggurl(url)
        self.assertEqual(repr(['S2J', 'null', 'nut', 'Casper', 'MegaXmas', 'Asashi', 'salami', 'PeachIcedT', 'El Pintor', 'Top100', 'Aero', 'Rat', 's-f', 'Badboi', 'Tern', 'Faint', 'John', 'Pipe', 'CJ', 'Fire', 'boback', 'Catface', 'mathandsurf', 'Nicko', 'DieselD', 'gahtto', 'Cream', 'REED', 'gardens', 'Crandle', 'xDankMemer', 'markrevival', 'Khayman', 'FredOG', 'Charlatan', 'Dimple', 'TAQUITO', 'Shura', 'Am2r', 'Swill', 'Burns', 'Digiornos', 'skreww L00se', 'Provider', 'ANDY2k', 'bren', 'Griff', 'Dumpage', 'shoegayze', 'Aned']), repr(actual))

    def test7entrants_startggurl_long(self):
        url = 'https://www.start.gg/tournament/melee-verdugo-west-145/event/melee-singles/overview'
        actual = importplayers.entrants_startggurl(url)
        self.assertEqual(repr(['S2J', 'null', 'nut', 'Casper', 'MegaXmas', 'Asashi', 'salami', 'PeachIcedT', 'El Pintor', 'Top100', 'Aero', 'Rat', 's-f', 'Badboi', 'Tern', 'Faint', 'John', 'Pipe', 'CJ', 'Fire', 'boback', 'Catface', 'mathandsurf', 'Nicko', 'DieselD', 'gahtto', 'Cream', 'REED', 'gardens', 'Crandle', 'xDankMemer', 'markrevival', 'Khayman', 'FredOG', 'Charlatan', 'Dimple', 'TAQUITO', 'Shura', 'Am2r', 'Swill', 'Burns', 'Digiornos', 'skreww L00se', 'Provider', 'ANDY2k', 'bren', 'Griff', 'Dumpage', 'shoegayze', 'Aned']), repr(actual))


if __name__ == '__main__':
    unittest.main()
