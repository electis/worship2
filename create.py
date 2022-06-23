import glob
import json
import os
import random

from environs import Env
import ffmpeg

# ffmpeg -loglevel error -y -re -loop 1 -f image2
# -i /storage/download/music/worship.jpg -i /storage/download/music/worship/77f69e67-c78f-44d8-bb47-5f0768396879.mp3
# -vf drawtext=text='Река - Gracetime Worship Band':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=4:x=(w-text_w)/2:y=h*11/12+(32)*1, drawtext=text='На пути откровений Твоих я радуюсь, как во всяком богатстве.':fontcolor=yellow:fontsize=32:box=1:boxcolor=black@0.5:boxborderw=4:x=(w-text_w)/2:y=h*1/16+(40)*1, drawtext=text='Псалтирь 118\:14':fontcolor=yellow:fontsize=32:box=1:boxcolor=black@0.5:boxborderw=4:x=(w-text_w)/2:y=h*1/16+(40)*2
# -codec:a aac -b:a 128k -ar 44100 -maxrate 2000k -bufsize 1000k -shortest -strict experimental -f flv rtmp://a.rtmp.youtube.com/live2/jmgf-2amh-19wg-h0rb-2hks


# ffmpeg -y -re -loop 1 -f image2
# -i /storage/download/music/worship.jpg
# -i /storage/download/music/worship/77f69e67-c78f-44d8-bb47-5f0768396879.mp3
# -vf drawtext=text='Рек'
# -codec:a aac -b:a 128k -ar 44100 -maxrate 4000k -bufsize 1000k -shortest -strict experimental -f flv out.mp4

def create():
    bible_file = 'bible.txt'
    video_file = '/storage/download/music/worship.mp4'
    audio_path = '/storage/download/music/worship/*.mp3'
    tmp_path = '/storage/download/music/tmp'
    video_params = dict(hwaccel_output_format='cuda')
    output_params = dict(bufsize='1000K', acodec='aac', vcodec='h264_nvenc')

    audio_files = glob.glob(audio_path)
    random.shuffle(audio_files)

    # TODO delete files in tmp_path

    with open(bible_file) as f:
        bible = json.load(f)
    random.shuffle(bible)

    playing_time = 0
    ff_video_src = ffmpeg.input(video_file, **video_params)
    for num, audio in enumerate(audio_files):
        pray_text = random.choice(bible[num])
        playing = TinyTag.get(audio)
        playing = f"{getattr(playing, 'title', '')} - {getattr(playing, 'artist', '')}"

        ff_video = ff_video_src.drawtext(pray_text, x=100, y=100, fontcolor='yellow', fontsize=32)  # escape_text=True
        ff_video = ff_video.drawtext(playing, x=100, y=1000, fontcolor='white', fontsize=20)

        ff_audio = ffmpeg.input(audio)
        out_file = os.path.join(tmp_path, f'{num:02d}.mp4')
        ffmpeg.output(ff_video, ff_audio, out_file, **output_params).overwrite_output().run()

        playing_time += ...
        if playing_time > 5400:
            break


if __name__ == '__main__':
    create()
