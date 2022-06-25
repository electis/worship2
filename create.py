import glob
import os
import random

from tinytag import TinyTag
import ffmpeg

from bible import bible
from conf import Config, read_config


def insert_line_breaks(text: str, max_length=80):
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


def create(conf: Config = None):
    if not conf:
        conf = read_config()

    video_params = dict(hwaccel_output_format='cuda')
    output_params = dict(acodec='aac', vcodec='h264_nvenc', f='flv', maxrate='1000k', bufsize='2000k')
    text_params = dict(box=1, boxcolor='black@0.5', x="(w-text_w)/2", boxborderw=15)

    audio_files = glob.glob(conf.audio_path)
    random.shuffle(audio_files)
    random.shuffle(bible)

    for f in glob.glob(os.path.join(conf.tmp_path, '*')):
        os.remove(f)

    playing_time = 0
    for num, audio in enumerate(audio_files):
        pray_text = insert_line_breaks(bible[num])
        pray_y = int(500 - len(pray_text.split('\n')) * (40 / 2 + 4)) if conf.pray_top is None else conf.pray_top
        playing = TinyTag.get(audio)
        playing_text = f"{getattr(playing, 'title', '')} - {getattr(playing, 'artist', '')}"

        loops = playing.duration // conf.video_len
        ff_video_src = ffmpeg.input(conf.video_file, stream_loop=loops, **video_params)
        ff_audio = ffmpeg.input(audio)
        ff_video = ff_video_src.drawtext(
            pray_text, y=pray_y, fontcolor='yellow', fontsize=40, **text_params
        ).drawtext(
            playing_text, y=1030, fontcolor='white', fontsize=32, **text_params
        )
        out_file = os.path.join(conf.tmp_path, f'{num:03d}.mp4')

        ffmpeg.output(ff_video, ff_audio, out_file, **output_params).overwrite_output().run()

        playing_time += playing.duration
        if playing_time > conf.stop_after:
            break


if __name__ == '__main__':
    create()
