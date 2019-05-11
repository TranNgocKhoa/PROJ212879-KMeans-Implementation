
import numpy as np
import random
import matplotlib.pyplot as plt
np.seterr(divide='ignore', invalid='ignore')


class Kmeans:
    def __init__(self, fname, n_clusters):
        self.fname = fname
        self.n_clusters = n_clusters
        self.input_array = np.loadtxt(fname)
        #self.input_array = np.asarray(self.input_data(fname))
                  #for X, Y, Z in csv.reader(open('targets.csv'))])
        self.label_array = np.zeros(self.input_array.shape, int)
        self.center_array = np.array(random.sample(self.input_array.tolist(), n_clusters))

        print(self.center_array)
        self.distance_square_array = np.ones([self.input_array.shape[0], n_clusters])
        self.cost = []
        self.init_center()
        # self.mu = np.mean(self.input_array, axis=0)
        # self.sigma = np.std(self.input_array, axis=0)
        # self.input_array1 = self.input_array
        # self.input_array = (self.input_array - self.mu) / self.sigma

    def init_center(self):
        curr_center_array = np.zeros([self.n_clusters, self.input_array.shape[1]])
        curr_center_array[0] = self.center_array[0]
        curr_distance_square_array = np.zeros([self.input_array.shape[0], 0])
        for i in range(self.n_clusters-1):


            curr_distance_square_array = np.append(curr_distance_square_array, np.zeros([self.input_array.shape[0], 1]), axis=1)
            curr_distance_square_array = self.compute_distance_square_all1(curr_center_array, curr_distance_square_array, i+1)
            self.update_label1(curr_distance_square_array)
            #find max distance by label
            Dk = curr_distance_square_array[self.label_array == 0, :]
            Xk = self.input_array[self.label_array == 0, :]
            max = np.max(Dk[:, 0], axis=0)
            XMax = Xk[np.argmax(Dk[:, 0], axis=0)]
            for j in range(i):
                Dk = curr_distance_square_array[self.label_array == j, :]
                Xk = self.input_array[self.label_array == j, :]
                if max < np.max(Dk[:, j], axis=0):
                    max = np.max(Dk[:, j], axis=0)
                    XMax = Xk[np.argmax(Dk[:, j], axis=0)]
            curr_center_array[i+1] = XMax


        # Dk = curr_distance_square_array[self.label_array == 0, :]
        # Xk = self.input_array[self.label_array == 0, :]
        #
        # curr_center_array[1] = Xk[np.argmax(Dk, axis=0)]
        #
        # print (curr_center_array)
        #
        # curr_distance_square_array = np.append(curr_distance_square_array, np.zeros([self.input_array.shape[0], 1]), axis=1)
        # curr_distance_square_array = self.compute_distance_square_all(curr_center_array, curr_distance_square_array, 2)
        # self.update_label(curr_distance_square_array)
        #
        # Dk = curr_distance_square_array[self.label_array == 0, :]
        # Xk = self.input_array[self.label_array == 0, :]
        #
        # max = np.max(Dk[:,0], axis=0)
        # XMax = Xk[np.argmax(Dk[:,0], axis=0)]
        # Dk = curr_distance_square_array[self.label_array == 1, :]
        # Xk = self.input_array[self.label_array == 1, :]
        #
        # if max < np.max(Dk[:,1], axis=0):
        #     max = np.max(Dk[:,1], axis=0)
        #     XMax = Xk[np.argmax(Dk[:,1], axis=0)]
        #
        # curr_center_array[2] = XMax
        self.center_array = curr_center_array
        print(curr_center_array)


    def kmeans(self):
        while True:
            self.compute_distance_square_all()
            self.update_label()
            new_centers = self.update_centers()
            if self.has_converged(new_centers):
                break
            self.center_array = new_centers
        self.cost = self.compute_cost()

    def input_data(self, fname):
        X = []
        with open(fname) as fileobject:
            for line in fileobject:
                Xi = [float(n) for n in line.strip()]
                X.append(Xi)
        return X

    def result(self):
        str_ = ''
        str_ += "Center was found by algorithm:\n\n"
        for center in self.center_array:
            str_ += str(center) + " "
            str_ += "\n"
        str_ += "\n"
        str_ += "Cost for this run:\n"
        str_ += str(sum(self.cost))
        return str_

    def compute_distance_square_all(self):
        i = 0
        for point in self.input_array:
            j = 0
            for center in self.center_array:
                self.distance_square_array[i][j] = self.compute_distance_square(point, center)
                j += 1
            i += 1

    def compute_distance_square_all1(self, center_array, distance_square_array, n_cluster):
        i = 0
        for point in self.input_array:


            distance_square_array[i][n_cluster-1] = self.compute_distance_square(point, center_array[n_cluster-1])
            i += 1
        return distance_square_array

    def plot(self):
        plt.show(block=False)
        fig = plt.figure()
        # mu = np.mean(self.input_array)
        # sigma = np.std(self.input_array)
        # X_norm = (self.input_array - mu) / sigma
        color_array = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', '#E9967A']
        marker_array = ["3",",","o","v","^","<",">","1","2",".","4","8","s","p","P"]
        X_list = []
        ax = fig.add_subplot(111, projection='3d')
        for i in range(self.n_clusters):
            Xi = self.input_array[self.label_array == i, :]
            #Xi = X_norm[self.label_array == i, :]
            X_list.append(Xi)

        for i in range(self.n_clusters):
            ax.scatter(X_list[i][:, 0], X_list[i][:, 1], X_list[i][:, 2], c=color_array[i], marker=marker_array[i])
        return plt


    def update_label(self):
        self.label_array = np.argmin(self.distance_square_array, axis=1)
    def update_label1(self, distance_square_array):
        self.label_array = np.argmin(distance_square_array, axis=1)

    def has_converged(self, new_centers):
        return (set([tuple(a) for a in self.center_array]) ==
                set([tuple(a) for a in new_centers]))

    def update_centers(self):
        centers = np.zeros((self.n_clusters, self.input_array.shape[1]))
        for k in range(self.n_clusters):
            Xk = self.input_array[self.label_array == k, :]
            if Xk.shape[0] == 0:
                continue
            centers[k, :] = np.mean(Xk, axis=0)
        return centers

    def compute_cost(self):
        cost_list = []
        for k in range(self.n_clusters):
            Xk = self.input_array[self.label_array == k, :]
            if Xk.shape[0] == 0:
                continue
            cost_list.append(sum(self.compute_distance_square(Xk[i],
                                                              self.center_array[k])
                                 for i in range(Xk.shape[0])))
        return cost_list

    def compute_distance_square(self, point1, point2):
        distance_square = 0
        for i in range(len(point1)):
            distance_square += (point1[i] - point2[i]) ** 2
        return distance_square

    def ouput_to_excel(self):
        import xlwt
        wb = xlwt.Workbook()
        ws = []
        rowindex = []
        for i in range(self.center_array.shape[0]):
            ws.append(wb.add_sheet("My Sheet" + " " + str(i)))
            rowindex.append(0)
        for i, row in enumerate(self.input_array):
            for j, col in enumerate(row):
                ws[self.label_array[i]].write(rowindex[self.label_array[i]], j, col)
            rowindex[self.label_array[i]] += 1
        wb.save("data_out.xls")

    def run100times(self):
        mincost = 0
        min_label_arr = np.zeros(self.input_array.shape, int)
        min_center_array = None
        for i in range(100):
            self.center_array = np.array(random.sample(self.input_array.tolist(), self.n_clusters))
            self.__init__(self.fname, self.n_clusters)
            self.kmeans()
            if i == 0:
                mincost = self.cost
                min_label_arr = self.label_array
                min_center_array = self.center_array
            else:
                if mincost > self.cost:
                    mincost = self.cost
                    min_label_arr = self.label_array
                    min_center_array = self.center_array
            print(mincost)
        self.label_array = min_label_arr
        self.cost = mincost
        self.center_array = min_center_array


# km = Kmeans("out.txt", 5)
# km.init_center()
# km.kmeans()
# print(km.result())