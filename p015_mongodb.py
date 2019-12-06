from pymongo import MongoClient
conn = MongoClient('mongodb://localhost:27017/')
db = conn.avIdol
db.col.insert([
    {"name": '波多野結衣', 'bwh': '{ "b": 90, "w": 59, "h": 85}' , 'age': 30},
    {"name": '吉泽明步', 'bwh': '{ "b": 86, "w": 58, "h": 86}' , 'age': 35},
    {"name": '桃乃木香奈', 'bwh': '{ "b": 80, "w": 54, "h": 80}' , 'age': 22},
    {"name": '西宫梦', 'bwh': '{ "b": 85, "w": 56, "h": 86}' , 'age': 22},
    {"name": '松下纱荣子', 'bwh': '{ "b": 88, "w": 57, "h": 86}' , 'age': 28}
])
#db.col.remove({"name": "波多野結衣"})   删除 波多野结衣
#db.col.remove()  删除全部
#db.col.update({'name': '吉泽明步'}, {'$set': {'name': '苍井空'}})  把 吉泽明步 换成 苍井空
for item in db.col.find():
    print(item)