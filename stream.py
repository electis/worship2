import glob
import logging
import os

import ffmpeg

from conf import Config, read_config
from helpers import log_ffmpeg, notify, post2group, post2vk_task

logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'worship.log'), level=logging.INFO,
    format='%(asctime)s %(levelname)s %(module)s.%(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
)


def stream(conf: Config):
    output_params = dict(f='flv', codec='copy')
    stream = f"{conf.stream_url}{'' if conf.stream_url.endswith('/') else '/'}{conf.stream_key}"
    in_file = os.path.join(conf.tmp_path, conf._in_file)

    with open(in_file, 'w') as file:
        file.writelines([f"file '{path}'\n"
                         for path in sorted(glob.glob(os.path.join(conf.tmp_path, '*.mp4')))])
    joined = ffmpeg.input(in_file, safe=0, format='concat', re=None)

    ff = ffmpeg.output(joined, stream, **output_params).overwrite_output()
    if conf.debug:
        logging.debug(' '.join(ff.get_args()))
    with log_ffmpeg(ff, conf):
        ff.run(cmd=conf.stream_cmd or 'ffmpeg', capture_stdout=True, capture_stderr=True)


if __name__ == '__main__':
    conf = read_config()
    with notify('Worship stream', conf.tg_, only_error=not(conf.debug)):
        post2group(conf)
        post2vk_task(conf)
        stream(conf)
