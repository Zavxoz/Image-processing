from math import pow, floor, sqrt
import numpy as np

class ImageObjectDetector:
    def __init__(self, image):
        self.sugar_min = 400
        self.sugar_max = 850
        self.spoon_min = 1700
        self.spoon_max = 3900
        self.image = image
        self.width = image.size[0]
        self.height = image.size[1]
        self.labels = [[0] * self.height for i in range(self.width)]
        self.equality_table = []
        self.squares = []
        self.perimeters = []
        self.densities = []
        self.tuples = []
        self.cluster1 = []
        self.cluster2 = []
        self.areas = 0

    def labeling(self):
        for i in range(self.width):
            for j in range(self.height):
                self.__fill(i, j)
        self.__check()
        self.__relabeling()
        self.areas = len(self.equality_table)
        self.squares = [0 for i in range(self.areas)]
        self.perimeters = [0 for i in range(self.areas)]
        self.densities = [0 for i in range(self.areas)]
        for i in range(self.width):
            for j in range(self.height):
                self.__refill_and_count_params(i, j)
        self.__count_densities()

    def __fill(self, x, y):
        if x > 0 and y > 0:
            left = self.labels[x - 1][y]
            upper = self.labels[x][y - 1]
        else:
            return
        if self.image.getpixel((x, y)) == 255:
            if left == 0 and upper == 0:
                self.areas += 1
                self.labels[x][y] = self.areas
                return
            if left > 0 and upper == 0:
                self.labels[x][y] = left
                return
            if left == 0 and upper > 0:
                self.labels[x][y] = upper
                return
            if left > 0 and upper > 0:
                if left == upper:
                    self.labels[x][y] = upper
                else:
                    self.labels[x][y] = left
                    self.__associate(upper, left)
                return

    def __check(self):
        a = []
        for i in range(len(self.equality_table)):
            for j in range(len(self.equality_table)):
                if i == j:
                    continue
                c1 = self.equality_table[i]
                c2 = self.equality_table[j]
                c3 = list(set(c1) & set(c2))
                if len(c3) > 0 and a.count([j, i]) == 0:
                    a.append([i, j])
        a.reverse()
        if len(a) > 0:
            for i in range(len(a)):
                self.equality_table[a[i][0]].extend(self.equality_table[a[i][1]])
                self.equality_table[a[i][1]].clear()
                self.equality_table.remove([])

    def __refill_and_count_params(self, x, y):
        for it in range(len(self.equality_table)):
            if self.equality_table[it].count(self.labels[x][y]) > 0:
                self.labels[x][y] = it + 1
                self.squares[it] += 1
                if self.__check_if_edge(x, y) == 0:
                    self.perimeters[it] += 1
                return

    def __check_if_edge(self, x, y):
        if 0 < x < self.width - 1 and 0 < y < self.height - 1:
            return min(self.labels[x - 1][y - 1],
                       self.labels[x - 1][y + 1],
                       self.labels[x + 1][y - 1],
                       self.labels[x + 1][y + 1],
                       self.labels[x - 1][y],
                       self.labels[x][y - 1],
                       self.labels[x][y + 1],
                       self.labels[x + 1][y])

    def __relabeling(self):
        for i in range(self.areas + 1):
            for j in range(len(self.equality_table)):
                if i > 0:
                    if self.equality_table[j].count(i) > 0:
                        break
                    elif j == len(self.equality_table) - 1:
                        self.equality_table.append([i])
                        break

    def __associate(self, area1, area2):
        if len(self.equality_table) == 0:
            self.equality_table.append([area1, area2])
        for it in range(len(self.equality_table)):
            if self.equality_table[it].count(area1) > 0 and \
               self.equality_table[it].count(area2) > 0:
                return
            if self.equality_table[it].count(area1) > 0 and \
               self.equality_table[it].count(area2) == 0:
                self.equality_table[it].append(area2)
                return
            if self.equality_table[it].count(area2) > 0 and \
               self.equality_table[it].count(area1) == 0:
                self.equality_table[it].append(area1)
                return
            if self.equality_table[it].count(area1) == 0 and \
               self.equality_table[it].count(area2) == 0 and \
               it == len(self.equality_table) - 1:
                self.equality_table.append([area1, area2])
                return

    def __count_densities(self):
        for i in range(len(self.densities)):
            self.densities[i] = pow(self.perimeters[i], 2) / self.squares[i]
    
    def __get_tuples(self):
        for i in range(self.areas):
            if (self.sugar_min < self.squares[i] < self.sugar_max or self.spoon_min < self.squares[i] < self.spoon_max):
                self.tuples.append([self.squares[i], self.perimeters[i], self.densities[i]])

    def show(self):
        self.image.show()

    def kmedians(self):
        self.__get_tuples()
        print(len(self.tuples), self.tuples)
        center1 = [350, 55, 10]
        center2 = [70, 12, 2]
        for i in range(100):
            list1 = [[], [], []]
            list2 = [[], [], []]
            self.cluster1.clear()
            self.cluster2.clear()
            for j in range(len(self.tuples)):
                rng1 = sqrt(pow(center1[0] - self.tuples[j][0], 2) +
                            pow(center1[1] - self.tuples[j][1], 2) +
                            pow(center1[2] - self.tuples[j][2], 2))
                rng2 = sqrt(pow(center2[0] - self.tuples[j][0], 2) +
                            pow(center2[1] - self.tuples[j][1], 2) +
                            pow(center2[2] - self.tuples[j][2], 2))
                if rng1 < rng2:
                    self.cluster2.append(self.tuples[j])
                    list2[0].append(self.tuples[j][0])
                    list2[1].append(self.tuples[j][1])
                    list2[2].append(self.tuples[j][2])
                else:
                    self.cluster1.append(self.tuples[j])
                    list1[0].append(self.tuples[j][0])
                    list1[1].append(self.tuples[j][1])
                    list1[2].append(self.tuples[j][2])
            for j in range(len(center1)):
                center1 = [np.median(list1[0]), np.median(list1[1]), np.median(list1[2])]
                center2 = [np.median(list2[0]), np.median(list2[1]), np.median(list2[2])]
        print("Spoons:", len(self.cluster1))
        print("Sugar:", len(self.cluster2))

    def colorize_clusters(self):
        cluster1colors = []
        cluster2colors = []
        self.image = self.image.convert('RGB')
        for i in range(len(self.cluster1)):
            cluster1colors.append(self.densities.index(self.cluster1[i][2]) + 1)
        for i in range(len(self.cluster2)):
            cluster2colors.append(self.densities.index(self.cluster2[i][2]) + 1)
        for i in range(self.width):
            for j in range(self.height):
                if self.image.getpixel((i, j)) == (255, 255, 255):
                    if cluster1colors.count(self.labels[i][j]) > 0:
                        self.image.putpixel((i, j), (255, 0, 0))
                    if cluster2colors.count(self.labels[i][j]) > 0:
                        self.image.putpixel((i, j), (0, 255,0))
