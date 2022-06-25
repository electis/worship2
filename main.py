import os.path

from conf import read_config
from stream import stream
from create import create


def choice():
    config = read_config()
    if os.path.exists(os.path.join(config.tmp_path, config._in_file)):
        stream(config)
    else:
        create(config)


if __name__ == '__main__':
    choice()
