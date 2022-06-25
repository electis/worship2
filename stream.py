import glob
import os

import ffmpeg

from conf import Config, read_config


def stream(conf: Config = None):
    if not conf:
        conf = read_config()
    output_params = dict(f='flv', codec='copy')
    stream = f"{conf.stream_url}{'' if conf.stream_url.endswith('/') else '/'}{conf.stream_key}"
    in_file = os.path.join(conf.tmp_path, conf._in_file)

    with open(in_file, 'w') as file:
        file.writelines([f"file '{path}'\n"
                         for path in sorted(glob.glob(os.path.join(conf.tmp_path, '*.mp4')))])
    joined = ffmpeg.input(in_file, safe=0, format='concat', readrate=1)

    ffmpeg.output(joined, stream, **output_params).overwrite_output().run(cmd=conf.stream_cmd or 'ffmpeg')


if __name__ == '__main__':
    stream()
