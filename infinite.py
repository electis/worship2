import glob
import logging
import os
import random

import ffmpeg

from bible import bible
from conf import Config, read_config
from create import get_playing_text, insert_line_breaks
from helpers import log_ffmpeg

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(module)s.%(funcName)s: %(message)s',
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S', handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'infinite.log')),
        logging.StreamHandler()
    ]
)

def stream(audio, video, output_params, conf: Config):
    stream = f"{conf.stream_url}{'' if conf.stream_url.endswith('/') else '/'}{conf.stream_key}"
    ff = ffmpeg.output(video, audio, stream, **output_params).overwrite_output()
    if conf.debug:
        logging.debug(' '.join(ff.get_args()))
    return ff


def proceed_stream():
    logging.info('proceed_stream')
    video_params = dict(re=None)
    # video_params = dict(hwaccel_output_format='cuda')
    output_params = dict(acodec='aac', vcodec='libx264', f='flv', maxrate='3000k', bufsize='6000k', shortest=None)
    process = None
    while True:
        conf = read_config()
        output_params.update({
            'b:v': '3000k', 'b:a': '128k', 'ar': '44100', 'framerate': '30', 'g': '30',
            'threads': conf.threads
        })
        audio_files = glob.glob(conf.audio_path)
        random.shuffle(audio_files)
        random.shuffle(bible)
        for num, audio in enumerate(audio_files):
            logging.info(f'playing {audio} {num}/{len(audio_files)}')
            pray_text = bible[num]

            if len(pray_text) < 550:
                max_length = 58
                font_size = 56
            else:
                max_length = 64
                font_size = 50
            pray_text = insert_line_breaks(pray_text, max_length=max_length)
            pray_y = int(500 - len(pray_text.split('\n')) * (40 / 2 + 4)) if conf.pray_top is None else conf.pray_top
            playing_text, duration = get_playing_text(audio)

            ff_audio = ffmpeg.input(audio, vn=None)
            ff_video_src = ffmpeg.input(conf.video_file, stream_loop=-1, **video_params)

            ff_video = ff_video_src.drawtext(
                pray_text, y=pray_y, fontcolor='white', fontsize=font_size, x="(w-text_w)/2", shadowx=2, shadowy=2
            ).drawtext(
                playing_text, y=1020, fontcolor='white', fontsize=32, x=600
            )
            ff = stream(ff_audio, ff_video, output_params, conf)

            if process:
                # with log_ffmpeg(ff, conf):
                process.wait()
            # TODO vk тормозит
            process = ff.run_async(cmd=conf.stream_cmd or 'ffmpeg', pipe_stdout=True)


if __name__ == '__main__':
    proceed_stream()
