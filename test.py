import unittest

from conf import read_config
from vk import post2vk


class TestPost2VK(unittest.TestCase):

    def test_post2vk(self):
        # run stream first!
        conf = read_config()
        conf.vk_.group_id = '-143175846'
        result = post2vk(conf, data_file='test_post2vk.json')
        self.assertTrue(result)


class TestMethod(unittest.TestCase):

    def test_insert_line_breaks(self):
        from create import insert_line_breaks
        from bible5 import bible

        # print(insert_line_breaks(bible[0] + '\n'))
        # print(insert_line_breaks(bible[0] + ' '))
        for b in bible:
            print(insert_line_breaks(b))


if __name__ == '__main__':
    unittest.main()
