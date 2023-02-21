import json

import chardet
import numpy as np
import matplotlib.pyplot as plt
import sys
import base64
import redis
from sko.GA import GA_TSP

# num_points = 3
# tsp_name = sys.argv[1] if len(sys.argv) > 1 else 'data/tsp.csv'
# file_name = sys.argv[1] if len(sys.argv) > 1 else 'data/nctu.csv'
# points_coordinate = np.loadtxt(file_name, delimiter=',')
# start_point = [[0, 0]]
# end_point = [[6, 0]]
#
# distance_matrix = np.loadtxt(tsp_name)
# points_coordinate = np.concatenate([points_coordinate, start_point, end_point])
# # distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')
# print(points_coordinate)
# print(distance_matrix)
#
#
# def cal_total_distance(routine):
#     '''The objective function. input routine, return total distance.
#     cal_total_distance(np.arange(num_points))
#     '''
#     num_points, = routine.shape
#     # start_point,end_point 本身不参与优化。给一个固定的值，参与计算总路径
#     routine = np.concatenate([[num_points], routine, [num_points + 1]])
#     return sum([distance_matrix[routine[i], routine[i + 1]] for i in range(num_points + 2 - 1)])
#
#
# ga_tsp = GA_TSP(func=cal_total_distance, n_dim=num_points, size_pop=50, max_iter=500, prob_mut=1)
# best_points, best_distance = ga_tsp.run()
# print(best_points, best_distance)
#
# fig, ax = plt.subplots(1, 2)
# best_points_ = np.concatenate([[num_points], best_points, [num_points + 1]])
# best_points_coordinate = points_coordinate[best_points_, :]
# ax[0].plot(best_points_coordinate[:, 0], best_points_coordinate[:, 1], 'o-r')
# ax[1].plot(ga_tsp.generation_best_Y)
# plt.show()

points_coordinate = [{"order_id":0, "name":"中文"}, {"order_id":1}, {"order_id":2}, {"order_id":3}, {"order_id":4}]
r = redis.StrictRedis(host='172.24.X.X', port=6149, password="XXXXXXXX", decode_responses=True)
str = base64.b64encode(json.dumps(points_coordinate).encode(encoding="utf-8"))
r.set('foo', str)
ret = r.get('foo')
print( base64.b64decode(ret))
