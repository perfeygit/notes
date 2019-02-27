import redis

r = redis.Redis(host='127.0.0.1', port=6379)


# print(r.keys("*"))
# print(r.llen('data'))  # llen()  列表类型的数量
# print(r.type("data"))
# print(r.lpop('data').decode('utf-8'))
def list_iter(name):
    """
    自定义redis列表增量迭代
    :param name: redis中的name，即：迭代name对应的列表
    :return: yield 返回 列表元素
    """
    list_count = r.llen(name)
    for index in range(list_count):
        yield r.lindex(name, index)


# 使用
# for item in list_iter('data'):
#     print(item.decode())
for key in r.keys("*"):
    print("类型:"+ r.type(key).decode(),"键:"+ key.decode())
    if r.type(key) == b'string':
        print('字符串',r.get(key))
    if r.type(key) == b'list':
        print('列表数量 '+key.decode()+':'+str(r.llen(key)))
        for item in list_iter(key):
            print('列表',item.decode())
    if r.type(key) == b'hash':
        print('字典数量 ' + key.decode() + ':' + str(r.hlen(key)),'字典键:',r.hkeys(key))
        # print(r.hget(key,'age'))    # 获取键对应的值
        # print('字典',r.hgetall(key))  # 一下获取字典所有键值对(可能会撑爆内存)
        for item in r.hscan_iter(key):
            print('字典',item)
    if r.type(key) == b'zset':
        print('有序集合数量:',r.zcard(key))
        for item in r.zscan_iter(key):
            print('有序集合',item)


