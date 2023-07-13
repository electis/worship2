import json
import time
from datetime import datetime
from threading import Thread

import vk_api

from conf import Config
from helpers import notify, logging


def get_api(access_token):
    vk_session = vk_api.VkApi(token=access_token)
    return vk_session.get_api()


def get_live(api, owner_id, last=10):
    videos = api.video.get(owner_id=owner_id, count=last)

    video = None
    now = datetime.now()
    for video in videos.get('items', []):
        live_status = video.get('live_status')
        date = datetime.fromtimestamp(video['date']).date()
        if live_status == 'started' and date == now.date():
            break
        video = None

    return video


def post_wall(api, owner_id, message=None, attachments=None, video=None, mute_notifications=1, from_group=1):
    # attachments = f"{type}{owner_id}_{media_id}"
    params = dict(
        from_group=from_group,
        mute_notifications=mute_notifications,
        owner_id=owner_id,
    )
    if message:
        params['message'] = message
    if attachments:
        params['attachments'] = attachments
    elif video:
        params['attachments'] = f"video{video['owner_id']}_{video['id']}"
    return api.wall.post(**params).get('post_id')


def load_data(filename):
    data = dict()
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError, TypeError) as exc:
        print(exc)
    return data


def save_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)


def del_msg(api, owner_id, post_id):
    return api.wall.delete(owner_id=owner_id, post_id=post_id)


def del_video(api, owner_id, video_id):
    return api.video.delete(video_id=video_id, owner_id=owner_id, target_id=owner_id)


def post2vk(conf: Config, data_file='post2vk.json', delay=0):
    time.sleep(delay)
    with notify('post2vk'):
        api = get_api(conf.vk_.access_token)
        video = get_live(api, conf.vk_.group_id)
        if video:
            post_id = post_wall(api, conf.vk_.group_id, video=video)
            data = load_data(data_file)

            try:
                if old_post_id := data.get('post_id'):
                    del_msg(api, conf.vk_.group_id, old_post_id)
                if old_video_id := data.get('video_id'):
                    del_video(api, conf.vk_.group_id, old_video_id)
            except Exception as exc:
                logging.exception(f'post2vk: Exception {exc}')

            data['post_id'] = post_id
            data['video_id'] = video['id']
            save_data(data, data_file)
            return True
        logging.warning('post2vk: live video not found')

def post2vk_task(conf: Config):
    task = Thread(target=post2vk, kwargs=dict(conf=conf, delay=10))
    task.start()
    return task
