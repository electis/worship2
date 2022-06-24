import glob
import os
import random
from typing import Union

from tinytag import TinyTag
from environs import Env
import ffmpeg

from bible import bible


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
        # if char == ':':
        #     result += '\:'
        # else:
        result += char
    return result


def create():
    pray_top: Union[int, None] = 150  # если None, то по центру
    stop_after = 90 * 60
    video_file = '/storage/download/music/worship.mp4'
    video_len = 8  # с запасом, чтобы звук раньше не кончился
    audio_path = '/storage/download/music/worship/*.mp3'
    tmp_path = '/storage/download/music/tmp'

    video_params = dict(hwaccel_output_format='cuda')
    output_params = dict(bufsize='1000K', acodec='aac', vcodec='h264_nvenc')
    text_params = dict(box=1, boxcolor='black@0.5', x="(w-text_w)/2", boxborderw=4)

    audio_files = glob.glob(audio_path)
    random.shuffle(audio_files)
    random.shuffle(bible)

    for f in glob.glob(os.path.join(tmp_path, '*')):
        os.remove(f)

    playing_time = 0
    for num, audio in enumerate(audio_files):
        pray_text = insert_line_breaks(bible[num])
        pray_y = int(500 - len(pray_text.split('\n')) * (40 / 2 + 4)) if pray_top is None else pray_top
        playing = TinyTag.get(audio)
        playing_text = f"{getattr(playing, 'title', '')} - {getattr(playing, 'artist', '')}"

        loops = playing.duration // video_len
        ff_video_src = ffmpeg.input(video_file, stream_loop=loops, **video_params)
        ff_audio = ffmpeg.input(audio)
        ff_video = ff_video_src.drawtext(
            pray_text, y=pray_y, fontcolor='yellow', fontsize=40, **text_params
        ).drawtext(
            playing_text, y=1030, fontcolor='white', fontsize=32, **text_params
        )
        out_file = os.path.join(tmp_path, f'{num:03d}.mp4')

        ffmpeg.output(ff_video, ff_audio, out_file, **output_params).overwrite_output().run()

        playing_time += playing.duration
        if playing_time > stop_after:
            break


if __name__ == '__main__':
    create()
