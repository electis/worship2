import glob
import os
import random
import logging

from tinytag import TinyTag
import ffmpeg

from bible5 import bible
from conf import Config, read_config
from helpers import notify, log_ffmpeg

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(module)s.%(funcName)s: %(message)s',
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S', handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'worship.log')),
        logging.StreamHandler()
    ]
)


def insert_line_breaks(text: str, max_length=64):
    # if length > max_length: result[last_space] = '\n'
    result = ''
    length = cur = last_space = 0
    while cur < len(text):
        if text[cur] == ' ':
            last_space = cur
        if text[cur:cur + 1] == '\n':
            result += '\n'
            cur += 1
            length = 0
            continue
        if length >= max_length:
            result = result[:last_space] + '\n'
            cur = last_space + 1
            length = 0
        result += text[cur]
        cur += 1
        length += 1
    return result


def insert_line_breaks_old(text: str, max_length=64):
    result = ''
    length = 0
    for num, char in enumerate(text):
        if length > max_length - max_length * 0.2:
            if text[num] == ' ':
                result += '\n'
                length = 0
                char = ''
        elif length > max_length:
            result += '\n'
            length = 0
        if text[num:num + 1] == '\n':
            length = -1
        length += 1
        result += char
    return result


def get_playing_text(filepath):
    artist, title = '', ''
    try:
        artist, title = os.path.basename(filepath).split('-')
        title = title[:-4]
    except:
        pass
    playing = TinyTag.get(filepath)
    artist = getattr(playing, 'artist', '') or artist
    title = getattr(playing, 'title', '') or title
    duration = getattr(playing, 'duration', 0) or 0
    return f"{title} - {artist}", duration


def create(conf: Config):
    video_params = dict()
    # video_params = dict(hwaccel_output_format='cuda')
    output_params = dict(acodec='aac', vcodec='libx264', f='flv', maxrate='3000k', bufsize='6000k', shortest=None)
    output_params.update({
        'b:v': '3000k', 'b:a': '128k', 'ar': '44100', 'framerate': '30', 'g': '30',
        'threads': conf.threads, 'profile': 'baseline',
    })
    # text_params = dict(box=1, boxcolor='black@0.5', x="(w-text_w)/2", boxborderw=15)

    audio_files = glob.glob(conf.audio_path)
    random.shuffle(audio_files)

    for f in glob.glob(os.path.join(conf.tmp_path, '*')):
        os.remove(f)

    random.shuffle(bible)
    # bible.sort(key=len, reverse=True)

    playing_time = 0
    for num, audio in enumerate(audio_files):
        pray_text = bible[num]

        if len(pray_text) < 550:
            max_length = 60
            font_size = 56
        else:
            max_length = 68
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
        out_file = os.path.join(conf.tmp_path, f'{num:03d}.mp4')

        ff = ffmpeg.output(ff_video, ff_audio, out_file, **output_params).overwrite_output()
        if conf.debug:
            logging.debug(' '.join(ff.get_args()))
        with log_ffmpeg(ff, conf) as result:
            ff.run(capture_stdout=True, capture_stderr=True)
        if result[0] is True:
            playing_time += duration
            if playing_time > conf.stop_after:
                break
        else:
            if os.path.exists(out_file):
                os.remove(out_file)

if __name__ == '__main__':
    conf = read_config()
    with notify('Worship create', only_error=not(conf.debug)):
        create(conf)
