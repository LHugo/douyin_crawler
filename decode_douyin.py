import json
from handle_db import insert_id, insert_uid


def response(flow):
    if 'aweme/v1/user/follower/list' in flow.request.url:
        for user in json.loads(flow.response.text)['followers']:
            douyin_id = {}
            douyin_uid = {}
            douyin_id['share_id'] = user['uid']
            douyin_uid['user_id'] = user['short_id']
            insert_id(douyin_id)
            insert_uid(douyin_uid)
