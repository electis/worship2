import glob
import logging
import os
import random

import ffmpeg

from bible import bible
from conf import read_config
from create import get_playing_text, insert_line_breaks

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(module)s.%(funcName)s: %(message)s',
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S', handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'infinite.log')),
        logging.StreamHandler()
    ]
)

def choice(items, last = None):
    item = random.choice(items)
    while item == last:
        item = random.choice(items)
    return item


def calc_font(text):
    if len(text) < 550:
        return  56, 58
    else:
        return 50, 64


def proceed_stream():
    logging.info('proceed_stream')
    conf = read_config()
    video_params = dict(hwaccel_output_format='cuda')
    # video_params = dict()
    create_params = dict(acodec='aac', vcodec='libx264', f='flv', maxrate='3000k', bufsize='6000k', shortest=None)
    create_params.update({
        'b:v': '3000k', 'b:a': '128k', 'ar': '44100', 'framerate': '30', 'g': '30',
        'threads': conf.threads
    })
    stream_params = dict(f='flv', codec='copy')

    for f in glob.glob(os.path.join(conf.tmp_path, '*')):
        os.remove(f)
    in_file = os.path.join(conf.tmp_path, conf._in_file)
    joined = ffmpeg.input(in_file, safe=0, format='concat', re=None)

    stream_url = f"{conf.stream_url}{'' if conf.stream_url.endswith('/') else '/'}{conf.stream_key}"
    creating = None
    text = audio = None
    num = 1
    audio_files = glob.glob(conf.audio_path)

    while True:
        audio = choice(audio_files, audio)
        text = choice(bible, text)
        font_size, max_length = calc_font(text)
        bible_text = insert_line_breaks(text, max_length=max_length)
        pray_y = int(500 - len(text.split('\n')) * (40 / 2 + 4)) if conf.pray_top is None else conf.pray_top
        playing_text, duration = get_playing_text(audio)
        ff_audio = ffmpeg.input(audio, vn=None)
        ff_video_src = ffmpeg.input(conf.video_file, stream_loop=-1, **video_params)
        ff_video = ff_video_src.drawtext(
            bible_text, y=pray_y, fontcolor='white', fontsize=font_size, x="(w-text_w)/2", shadowx=2, shadowy=2
        ).drawtext(
            playing_text, y=1020, fontcolor='white', fontsize=32, x=600
        )
        out_file = os.path.join(conf.tmp_path, f'{num:07d}.mp4')
        ff = ffmpeg.output(ff_video, ff_audio, out_file, **create_params).overwrite_output()
        if creating:
            creating.wait()
        creating = ff.run_async(cmd=conf.stream_cmd or 'ffmpeg', overwrite_output=True, quiet=True)

        with open(in_file, 'a') as file:
            print(f'file {out_file}', file=file)
        if num == 2:
            stream = ffmpeg.output(joined, stream_url, **stream_params).overwrite_output()
            stream.run_async(cmd=conf.stream_cmd or 'ffmpeg', overwrite_output=True)

        num += 1


if __name__ == '__main__':
    proceed_stream()
