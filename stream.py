import glob
import os

import ffmpeg

from conf import Config, read_config
from helpers import notify, post2group


def stream(conf: Config):
    output_params = dict(f='flv', codec='copy')
    stream = f"{conf.stream_url}{'' if conf.stream_url.endswith('/') else '/'}{conf.stream_key}"
    in_file = os.path.join(conf.tmp_path, conf._in_file)

    with open(in_file, 'w') as file:
        file.writelines([f"file '{path}'\n"
                         for path in sorted(glob.glob(os.path.join(conf.tmp_path, '*.mp4')))])
    joined = ffmpeg.input(in_file, safe=0, format='concat', re=None)

    ffmpeg.output(joined, stream, **output_params).overwrite_output().run(cmd=conf.stream_cmd or 'ffmpeg')


if __name__ == '__main__':
    conf = read_config()
    with notify('Worship stream', conf.tg_, only_error=not(conf.debug)):
        post2group(conf)
        stream(conf)
