import glob
import os
import logging

import ffmpeg

from conf import Config, read_config
from helpers import notify, post2group, log_tg

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
    try:
        ff.run(cmd=conf.stream_cmd or 'ffmpeg', capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as exc:
        logging.exception(exc)
        logging.error(' '.join(ff.get_args()))
        logging.error(f'stderr: {exc.stderr.decode("utf8")}')
        logging.error(f'stdout: {exc.stdout.decode("utf8")}')
        log_tg(str(exc), conf.tg_)
    except Exception as exc:
        logging.exception(exc)
        logging.error(' '.join(ff.get_args()))
        log_tg(str(exc), conf.tg_)


if __name__ == '__main__':
    conf = read_config()
    with notify('Worship stream', conf.tg_, only_error=not(conf.debug)):
        post2group(conf)
        stream(conf)
