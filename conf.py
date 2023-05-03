import inspect
from pathlib import Path
import sys
from typing import Optional

from environs import Env

from pydantic import BaseModel


class TG(BaseModel):
    tg_chat_id: Optional[str]
    tg_token: Optional[str]


class Post(BaseModel):
    task_url: Optional[str]
    task_token: Optional[str]
    youtube_channel: Optional[str]
    chat_id: Optional[str]


class Config(BaseModel):
    stream_url: str
    stream_key: str
    pray_top: Optional[int]
    stop_after: Optional[int]
    video_file: str
    audio_path: str
    tmp_path: str
    threads: int = 1
    stream_cmd: Optional[str]
    debug: bool
    tg_: Optional[TG]
    post_: Optional[Post]
    _in_file: str = 'input.txt'


def script_dir():
    current_frame = inspect.currentframe()
    if current_frame is None:
        raise RuntimeError("Could not get current call frame.")
    frame = current_frame.f_back
    assert frame is not None
    return Path(frame.f_code.co_filename).parent.resolve()


def read_config() -> Config:
    env = Env()
    cur_path = script_dir()
    env.read_env(str(cur_path / '.env.example'))
    env.read_env(override=True)
    if len(sys.argv) > 1:
        env.read_env(str(cur_path / sys.argv[1]), override=True)

    conf = Config(**{key: env(key.upper())
                     for key in Config.__fields__.keys()
                     if not key.endswith('_')})
    conf.stop_after = conf.stop_after * 60
    tg = TG(
        tg_chat_id=env('TGRAM_CHATID', None),
        tg_token=env('TGRAM_TOKEN', None),
    )
    if tg.tg_chat_id and tg.tg_token:
        conf.tg_ = tg
    post = Post(
        task_url=env('TASK_URL', None),
        task_token=env('TASK_TOKEN', None),
        youtube_channel=env('YOUTUBE_CHANNEL', None),
        chat_id=env('CHAT_ID', None),
    )
    if post.task_url:
        conf.post_ = post

    Path(conf.tmp_path).mkdir(parents=True, exist_ok=True)
    return conf
