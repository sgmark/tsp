#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 发布
import redis


class RedisHelper(object):
    def __init__(self, host, port, password):
        self.__conn = redis.Redis(host=host, port=port, password=password)  # 连接Redis
        self.channel = 'tsp'  # 定义名称

    def publish(self, msg):  # 定义发布方法
        self.__conn.publish(self.channel, msg)
        return True

    def subscribe(self):  # 定义订阅方法
        pub = self.__conn.pubsub()
        pub.subscribe(self.channel)
        pub.parse_response()
        return pub


data1 = '{"user_id":"500","num_points":3,"distance_matrix":[[0.0,8.0,4.0,5.0,5.0],[8.0,0.0,4.0,5.0,5.0],[4.0,4.0,0.0,' \
        '3.0,3.0],[5.0,5.0,3.0,0.0,6.0],[5.0,5.0,3.0,6.0,0.0]],"points_coordinate":[[3,4], [3,-4], [3,0], [0,0], [6,' \
        '0]],"raw_data":[{"order_id":0}, {"order_id":1}, {"order_id":2}, {"order_id":3}, {"order_id":4}]} '

data2 = '{"user_id":"500","num_points":3,"distance_matrix":[[0.0, 35275.0, 35382.0, 17619.0, 34327.0],[35275.0, 0.0, ' \
        '31444.0, 16546.0, 27452.0],[35382.0, 31444.0, 0.0, 36216.0, 5277.0],[17619.0, 16546.0, 36216.0, 0.0, ' \
        '32800.0],[34327.0, 27452.0, 5277.0, 32800.0, 0.0]],"points_coordinate":[[121.093216,31.260159], [121.248242,' \
        '31.103885], [121.422161,31.267293], [121.147855,31.162225], [121.418280,31.229892]], "raw_data":[{' \
        '"order_id":0}, {"order_id":1}, {"order_id":2}, {"order_id":3}, {"order_id":4}]} '

obj = RedisHelper('172.24.X.X', 6149, "XXXXXXXX")
obj.publish(data1)  # 发布
obj.publish(data2)  # 发布
