# -*- coding:utf-8 -*-

import struct
import csv
# from .Mark import Mark


class AgvCar(object):

    def __init__(self, agvfilename, turnfilename, distancefilename):
        self.agvfilename = agvfilename      # agv程序文件地址
        self.turnfilename = turnfilename    # 转弯配置文件地址
        self.distanfilename = distancefilename  # 聚类配置文件地址
        self.StationStartAddress = 179088   # 文件中储存ST站点的起始地址
        self.StationDict = {}               # 站点地址字典，key-mark号，value-station
        self.BranchStartAddress = 168288    # 文件中储存分叉点的起始地址
        self.BranchDict = {}                # 分叉点地址字典，key-mark号，value-branch
        self.MarkerOrderCountStartNumber = 16   # 文件中路径编号及路径经过mark点个数信息起始
        self.MarkerOrderStartNumber = 416   # 文件中路径储存区域起始地址
        self.Paths = []                     # 所有路径list
        self.Turn = {}                      # 转弯处下一点dict
        self.Distance = {}                  # 距离dict
        self.ReadFromAgv()
        self.ReadFromTrun()
        self.ReadDistance()

    def ReadFromAgv(self):                  # 从agv程序中读取数据
        with open(self.agvfilename, 'rb') as fileData:
            fileData.seek(self.StationStartAddress)
            for i in range(200):
                stationMarkNumber = struct.unpack("h", fileData.read(2))[0]     # 读取站点mark号
                stationDir = struct.unpack("B", fileData.read(1))[0]            # 读取站点方向
                fileData.read(1)                                                # 第四字节意义不明，暂不处理
                if stationMarkNumber == 0:
                    break
                self.StationDict[i+1] = '%s_%s' % (stationMarkNumber, stationDir)   #Mark(i+1, stationMarkNumber, stationDir)
            fileData.close()

        with open(self.agvfilename, 'rb') as fileData:
            fileData.seek(self.BranchStartAddress)
            for i in range(200):
                branchMarkNumber = struct.unpack("h", fileData.read(2))[0]      # 读取分岔点mark号
                branchDir = struct.unpack("B", fileData.read(1))[0]            # 读取分岔点方向
                fileData.read(1)                                                # 第四字节无意义
                if branchMarkNumber == 0:
                    break
                self.BranchDict[branchMarkNumber] = '%s_%s' % (branchMarkNumber, branchDir)   #Mark(i+1, branchMarkNumber, branchDir)
            fileData.close()

        with open(self.agvfilename, 'rb') as fileData:
            fileData.seek(self.MarkerOrderCountStartNumber)
            paths = []
            for i in range(200):
                markerOrderNumber = struct.unpack("B", fileData.read(1))[0]     # 读取路径标号
                markerOrderCount = struct.unpack("B", fileData.read(1))[0]      # 读取路径点个数
                if markerOrderNumber != 0 or markerOrderCount != 0:
                    paths.append((markerOrderNumber, markerOrderCount))
            for i in range(len(paths)):
                path = []
                for j in range(100):
                    markerNumber = struct.unpack("B", fileData.read(1))[0]      # 读取mark号
                    markerDirection = struct.unpack("B", fileData.read(1))[0]   # 读取mark方向
                    if markerNumber != 0:
                        path.append('%s_%s' % (markerNumber, 1 if markerDirection&0x80==0 else 2))
                    else:
                        fileData.read(2*(100-j-1))
                        break;
                if len(path) != 0:
                    self.Paths.append(path)
            fileData.close()

    def ReadFromTrun(self):                 # 从自制的turn.csv文件中读取转弯下一点数据
        with open(self.turnfilename, 'r') as fileData:
            reader = csv.reader(fileData, delimiter=',')
            goals = []
            for line in reader:
                if reader.line_num == 1:
                    goals = line[1:]
                else:
                    d = {}
                    for i in range(len(goals)):
                        d[goals[i]] = line[i+1]
                    self.Turn[line[0]] = d
            fileData.close()

    def ReadDistance(self):                 # 从自制的distance.csv文件中读取相邻两点距离数据
        with open(self.distanfilename, 'r') as fileData:
            reader = csv.reader(fileData, delimiter=',')
            for line in reader:
                a1 = int(line[0])
                a2 = int(line[1])
                if a1 > a2:
                    a1, a2 = a2, a1
                self.Distance[a1, a2] = int(line[2])
            fileData.close()

    def FindPath(self, start, end):         # 搜索起点至终点的最短路径
        path = []
        point = start
        path.append(point)
        while True:
            if point == end:
                break
            point = self.FindNextPoint(point, end)
            path.append(point)
            if len(path) >= 200:
                print('error')
                break
        return path

    def FindNextPoint(self, start, end):    # 搜索起点至终点的下一点
        for key, value in self.BranchDict.items():      # 遍历所有分岔点
            if start == value:                         # 如果起点是分岔点
                return self.Turn[start][end]           # 从分岔点转弯字典中查询下一点
        for path in self.Paths:                         # 如果起点不是分岔点，遍历所有路径
            if (start in path) and (path.index(start) < len(path)-1):        # 如果这条路径包含起点并且起点不是最后一点，则返回这条路径的下一点
                return path[path.index(start)+1]

    def CalcDistance(self, path):           # 计算给出路径的长度
        if len(path) < 2:
            return 0
        distance = 0
        for i in range(len(path)-1):
            a1 = int(path[i].split('_')[0])
            a2 = int(path[i+1].split('_')[0])
            if a1 > a2:
                a1, a2 = a2, a1
            distance = distance + self.Distance[(a1, a2)]
        return distance
