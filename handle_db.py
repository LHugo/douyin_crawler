import pymongo
from pymongo.collection import Collection
import pymysql


# def insert_mongodb(self):
#     id_collection = Collection(db, 'douyin_id')
#     with open('id_list.txt', 'r') as f:
#         for id in f.readlines():
#             id_dict = {}
#             id_dict['share_id'] = id.replace('\n', '')
#             id_collection.insert(id_dict)


def get_random_id():
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['douyin_id']
    id_collection = Collection(db, 'douyin_id')
    return id_collection.find_one_and_delete({})


def insert_id(item):
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['douyin_id']
    id_collection = Collection(db, 'douyin_id')
    id_collection.insert(item)


def get_random_uid():
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['douyin_uid']
    id_collection = Collection(db, 'douyin_uid')
    return id_collection.find_one_and_delete({})


def insert_uid(item):
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['douyin_uid']
    id_collection = Collection(db, 'douyin_uid')
    id_collection.insert(item)


def insert_mysql(user_info):
    connect = pymysql.connect('localhost', 'root', 'root', 'douyin_info', charset='utf8', use_unicode=True)
    cursor = connect.cursor()
    insert_sql = """
        INSERT INTO user_info(md5_id, nick_name, douyin_id, signature, location, constellation, focus_num, follower_num, 
                                praise_received, production_num, liked_num)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE signature=VALUES(signature), focus_num=VALUES(focus_num), follower_num=VALUES(follower_num), praise_received=VALUES(praise_received), production_num=VALUES(production_num), liked_num=VALUES(liked_num)
        """
    items = (user_info['md5_id'], user_info['nick_name'], user_info['douyin_id'], user_info['signature'],
             user_info['location'], user_info['constellation'], user_info['focus_num'], user_info['follower_num'],
             user_info['praise_received'], user_info['production_num'], user_info['liked_num'])
    cursor.execute(insert_sql, items)
    connect.commit()
