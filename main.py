import sys
import time
sys.setrecursionlimit(1000000)
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import random
import math
import pyqtgraph as pg
from operator import itemgetter
class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("2018080139hw3")
        self.pw = pg.PlotWidget()
        bt1=QAction("最短距离",self)
        bt1.triggered.connect(self.getdis)
        bt2 = QAction("随机生成点", self)
        bt2.triggered.connect(self.random_pair)
        self.toolbar=self.addToolBar("最短距离")
        self.toolbar.addAction(bt1)
        self.toolbar = self.addToolBar("随机生成点")
        self.toolbar.addAction(bt2)
        self.point_list=[]

        self.pw.setXRange(min=0,  # 最小值
                          max=100)  # 最大值
        # 设置Y轴 刻度 范围
        self.pw.setYRange(min=0,  # 最小值
                          max=100)  # 最大值
        # 背景色改为白色
        self.pw.setBackground('w')
        # 居中显示 PlotWidget
        self.setCentralWidget(self.pw)

        # 实时显示应该获取 PlotDataItem对象, 调用其setData方法，
        # 这样只重新plot该曲线，性能更高
        self.scatter = self.pw.plot(pen=None, symbol='o')

        self.i = 0
        self.x = []  # x轴的值
        self.new_point_x = 0
        self.y = []  # y轴的值
        self.new_point_y = 0

        self.current_distance=float('inf')
        self.setMouseTracking(False)
        self.scatter.scene().sigMouseMoved.connect(self.mouseover)
        self.scatter.scene().sigMouseClicked.connect(self.mouse_clicked)



    def updateData(self):
        self.scatter.setData(self.x, self.y)

        # 鼠标移动事件，用于获取精确坐标（好像鼠标单击的坐标不准确）

    def mouseover(self, pos):
        # 参数pos 是像素坐标，需要 转化为  刻度坐标
        act_pos = self.scatter.mapFromScene(pos)
        if type(act_pos) != QPointF:
            return
        # print("over_1:",act_pos.x(), act_pos.y())
        self.new_point_x = act_pos.x()
        self.new_point_y = act_pos.y()

        # 鼠标单击事件，用于鼠标单击后事件的处理，包括：
        # 1）添加新坐标

    def mouse_clicked(self, event):
        self.x.append(self.new_point_x)
        self.y.append(self.new_point_y)
        self.updateData()

    def sort_x(self,point_list):
        return sorted(point_list,key=itemgetter('x'))
    def sort_y(self,point_list):
        return sorted(point_list,key=itemgetter("y"))

    def get_distance(self, point_a, point_b):
        return math.sqrt((point_a["x"] - point_b["x"]) ** 2 + (point_a["y"] - point_b["y"]) ** 2)

    def get_closest(self,left,right):
        if left+1 ==right:
            distance = self.get_distance(self.point_list[left],self.point_list[right])
            if distance < self.current_distance:
                self.current_distance =distance
                self.point_1 = self.point_list[left]
                self.point_2 = self.point_list[right]
            return distance
        mid = (left + right) // 2  # 取x的中点
        dist1 = self.get_closest(left, mid)
        dist2 = self.get_closest(mid, right)
        dist = min(dist1, dist2)

        temp_list = []
        for i in range(left, right + 1):
            if math.fabs(self.point_list[i]["x"] - self.point_list[mid]["x"]) <= dist:
                temp_list.append(self.point_list[i])
        temp_list = self.sort_y(temp_list)
        temp_len = len(temp_list)
        for i in range(temp_len):
            for j in range(i + 1, temp_len):
                # 不超过六个点进入此循环
                if temp_list[j]['y'] - temp_list[i]['y'] < dist:
                    dist3 = self.get_distance(temp_list[i], temp_list[j])
                    dist = min(dist, dist3)
                    # 加入寻找最近点对的相关代码
                    if dist == dist3 and dist < self.current_distance:
                        self.current_distance = dist
                        self.point_1 = temp_list[i]
                        self.point_2 = temp_list[j]
                else:
                    break
        return dist
    def get_closest2(self):
        init_distance =float('inf')
        for i in range(len(self.point_list)):
            for j in range(i+1,len(self.point_list)):
                dis = self.get_distance(self.point_list[i], self.point_list[j])
                if dis < init_distance:
                    init_distance = dis
                    self.point_1 = self.point_list[i]
                    self.point_2 = self.point_list[j]
        return dis
    def getdis(self):
        self.point_list=[]
        for i in range(len(self.x)):
            point = {}
            point["x"] = self.x[i]
            point["y"] = self.y[i]
            self.point_list.append(point)
        self.point_list=self.sort_x(self.point_list)
        t0=time.time()
        result0=self.get_closest(0,len(self.point_list)-1)
        t1=time.time()-t0
        print("分治法最短距离为", result0,
              "最近点配为(%d,%d)" % (self.point_1['x'], self.point_1['y']),
              "和(%d,%d)" % (self.point_2['x'], self.point_2['y']), "耗时", t1)
        t2=time.time()
        result1=self.get_closest2()
        t3=time.time()-t2
        print("暴力法最短距离为", result1,
              "最近点配为(%d,%d)" % (self.point_1['x'], self.point_1['y']),
              "和(%d,%d)" % (self.point_2['x'], self.point_2['y']),"耗时",t3)


    def random_pair(self):
        self.point_list = []
        for i in range(100000):
            point ={}
            point["x"] = random.randint(0,100000000)
            point["y"] = random.randint(0,100000000)
            self.point_list.append(point)
        self.point_list = self.sort_x(self.point_list)
        t0 = time.time()
        result0 = self.get_closest(0, len(self.point_list) - 1)
        t1 = time.time() - t0
        print("分治法最短距离为", result0,
              "最近点配为(%d,%d)" % (self.point_1['x'], self.point_1['y']),
              "和(%d,%d)" % (self.point_2['x'], self.point_2['y']), "耗时", t1)
        #t2 = time.time()
        #result1 = self.get_closest2()
        #t3 = time.time() - t2
        #print("暴力法最短距离为", result1,
        #      "最近点配为(%d,%d)" % (self.point_1['x'], self.point_1['y']),
        #      "和(%d,%d)" % (self.point_2['x'], self.point_2['y']), "耗时", t3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())