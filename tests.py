from unittest import TestCase
import unittest
import data

class test_brackets(TestCase):
    def test1de(self):
        w = data.gen(16)
        l = data.genl(w)
        m = w[0].llink.wlink.wlink.wlink.wlink.wlink.wlink
        for r in range(1, 16):
            self.assertEqual(m,w[r].llink.wlink.wlink.wlink.wlink.wlink.wlink)
        self.assertEqual(m, w[15].wlink.wlink.wlink.llink.wlink)
    
    def test2genm(self):
        w = data.genm(['a','b','c','d'])
        self.assertEqual(w[0].part1.tag, 'a')
        self.assertEqual(w[0].part2.tag, 'd')
        self.assertEqual(w[1].part1.tag, 'b')
        self.assertEqual(w[1].part2.tag, 'c')
if __name__ == '__main__':
    unittest.main()
