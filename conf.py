import inspect
from pathlib import Path
from typing import Optional, List, NewType, Union

from environs import Env

from pydantic import BaseModel


class Config(BaseModel):
    stream_url: str
    stream_key: str
    pray_top: Optional[int]
    stop_after: Optional[int]
    video_file: str
    audio_path: str
    tmp_path: str
    stream_cmd: Optional[str]
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
    env.read_env(str(script_dir() / '.env.example'))
    env.read_env(override=True)
    conf = Config(**{key: env(key.upper()) for key in Config.__fields__.keys()})
    conf.stop_after = conf.stop_after * 60
    Path(conf.tmp_path).mkdir(parents=True, exist_ok=True)
    return conf
