"""
rem Простой вариант
set F1=drawtext=text='Ставим Лайк, my friend!':font=Arial:fontsize=100:y=100:x=300

rem С Анимацией
rem set F1=drawtext=text='Подписываемся на канал!':x=t*100:y=100:alpha=t+0.01:fontsize=100+n*1:fontfile=Lobster.ttf

rem С выводом в конкретное время
rem set F1=drawtext=text='Не забываем комментировать!':x=(W-tw)/2:y=(H-th)/2:fontsize=100:enable='between(t,3,7)':fontfile=Lobster.ttf

rem Переменные в тексте
rem set F1=drawtext=text='Подписчиков на канале %%{eif\:t*10 + rand(0,5)\:d}':font=Arial:fontsize=80:y=100:x=300

rem Больше анимации с альфа-каналом и цветом
rem set F1=drawtext=text='Впечатляющая мощь!':x=W-t*(W/10):y=100:alpha=t+0.01:fontsize=100+t*5:fontfile=Lobster.ttf:fontcolor=#DD0000

rem Используем файл с текстом
rem set F1=drawtext=textfile=text.txt:reload=0:fontsize=H/15:x=100:y=100:font=Consolas

rem Обводка и ещё анимация
rem set F1=drawtext=text='Фантазия кончилась..':fontsize=H/10:x=(W-tw)/2:y='H/2 + sin(t)*300':borderw=3:bordercolor=red:fontfile=Lobster.ttf:fontcolor=yellow

rem Коробка и ещё анимация
rem set F1=drawtext=text='Warning Bruzzers':fontsize=H/15:x=(W-tw)/2:y=(H-th)/2:boxcolor=yellow:box=1:line_spacing=20:boxborderw=50:borderw=2:bordercolor=#DD0000:fontfile=Lobster.ttf:fontcolor=orange

rem Коробка и ещё анимация
rem set F1=drawtext=text='Knock, knock, Neo..':fontsize=H/15:x=(W-tw)/2:y=(H-th)/2:shadowcolor=gray:shadowx=5:shadowy=5:boxcolor=yellow:box=1:line_spacing=20:boxborderw=50:borderw=2:bordercolor=#DD0000:fontfile=Lobster.ttf:fontcolor=orange


ffmpeg.exe ^
-f lavfi -i color=c=white:s=1920x1080 -loop 1 ^
-s "1920x1080" -t 10 ^
-filter_complex "%F1%" ^
-y out.mp4
"""
import ffmpeg


def print_hi():
    inp = ffmpeg.input('/storage/download/music/worship/Жанна Каратаева, Алексей Каратаев - Я знаю.mp3')
    vid = ffmpeg.input('/storage/download/music/worship.gif', stream_loop=-1)
    out = 'out.mp4'
    joined = ffmpeg.concat(vid.video, inp.audio, v=1, a=1)
    ffmpeg.output(joined, out).run()


if __name__ == '__main__':
    print_hi()
