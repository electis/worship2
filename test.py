import unittest

from conf import read_config
from vk import post2vk


class TestPost2VK(unittest.TestCase):

    def test_post2vk(self):
        conf = read_config()
        conf.vk_.group_id = '-143175846'
        result = post2vk(conf, data_file='test_post2vk.json')
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
