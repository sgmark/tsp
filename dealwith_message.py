# 处理消息
import json

import numpy as np
from sko.GA import GA_TSP


def cal_total_distance(routine):
    '''The objective function. input routine, return total distance.
    cal_total_distance(np.arange(num_points))
    '''
    num_points, = routine.shape
    # start_point,end_point 本身不参与优化。给一个固定的值，参与计算总路径
    routine = np.concatenate([[num_points], routine, [num_points + 1]])
    return sum([tsp_deal_message.distance_matrix[routine[i], routine[i + 1]] for i in range(num_points + 2 - 1)])


class tsp_deal_message:
    distance_matrix = None

    def __init__(self, message):
        # 司机id
        self.user_id = message['user_id']
        # 原始数据
        self.raw_data = message['raw_data']
        # 转换过后的数据
        self.converted_data = []
        # 转换过后的数据orderId(用户所能看到的位置)
        self.order_index = []
        # 需要前往的位置
        self.distance_matrix = np.concatenate([message['distance_matrix']])
        # 由各个位置距离所产生的邻接矩阵
        self.points_coordinate = np.concatenate([message['points_coordinate']])
        tsp_deal_message.distance_matrix = self.distance_matrix
        self.num_points = message['num_points']

    def deal_message(self):
        ga_tsp = GA_TSP(func=cal_total_distance, n_dim=self.num_points, size_pop=50, max_iter=500, prob_mut=1)
        best_points, best_distance = ga_tsp.run()
        print(best_points, best_distance)
        best_points_ = np.concatenate([[self.num_points], best_points, [self.num_points + 1]])
        # fig, ax = plt.subplots(1, 2)
        # best_points_coordinate = self.distance_matrix[best_points_, :]
        # ax[0].plot(best_points_coordinate[:, 0], best_points_coordinate[:, 1], 'o-r')
        # ax[1].plot(ga_tsp.generation_best_Y)
        # plt.show()

        # 根据排序，将原始数据转化为新的排序
        for best_points_i in best_points_:
            self.converted_data.append(self.raw_data[best_points_i])
        print(best_points_)
        # 循环转化过后的数据获取每个位置上的orderId
        # 即用户看到自己所在的位置
        for data in self.converted_data:
            if "orderId" in data:
                self.order_index.append(data['orderId'])

        return self.converted_data, self.order_index
