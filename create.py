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
    inp = ffmpeg.input('/storage/download/music/worship/Жанна Каратаева, Алексей Каратаев - Я знаю.mp3')
    vid = ffmpeg.input('/storage/download/music/worship.gif')
    out = 'out.mp4'
    ffmpeg.filter([inp, vid]).output(out).run()


if __name__ == '__main__':
    create()
