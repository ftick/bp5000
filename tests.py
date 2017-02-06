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

if __name__ == '__main__':
    unittest.main()
