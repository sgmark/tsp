# ！/usr/bin/env python
# coding=utf-8
import asyncio
import json
from loguru import logger
import time

import asyncio_redis
import redis

from dealwith_message import tsp_deal_message
logger.add('/logs/tsp.log',
           level='DEBUG',
           format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {file} - {line} - {message}',
           rotation="10 MB",
           retention="10 days")


async def main():
    # Create a new redis connection (this will also auto reconnect)
    # 初始化redis,从服务器上获取连接信息
    connection = await asyncio_redis.Connection.create(host='172.24.X.X', port=6149, password="XXXXXXXX")
    try:
        # Subscribe to a channel.
        subscriber = await connection.start_subscribe()
        await subscriber.subscribe(["tsp"])
        # Print published values in a while/true loop.
        while True:
            reply = await subscriber.next_published()
            text = json.loads(reply.value)
            logger.info(text)
            if 'user_id' in text:
                try:
                    deal_ = tsp_deal_message(text)
                    converted_data, order_index = deal_.deal_message()
                    print("best_points_:", converted_data, "best_distance:", order_index)
                    # 排序后放入redis
                    r = redis.StrictRedis(host='172.24.X.X', port=6149, password="XXXXXXXX", decode_responses=True)
                    r.set('foo', 'bar')
                    redis_key = 'path-planning:{a}:{b}'.format(a=time.strftime('%Y-%m-%d', time.localtime()),
                                                               b=text['user_id'])
                    redis_key_index = redis_key + ":index"
                    r.set(redis_key, json.dumps(converted_data))
                    r.set(redis_key_index, json.dumps(order_index))
                    r.expire(redis_key, 24 * 3600)
                    r.expire(redis_key_index, 24 * 3600)
                    logger.info(redis_key)
                    r.close()
                except:
                    print('异常!!!!!')
    finally:
        connection.close()
        logger.error("服务关闭");


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
