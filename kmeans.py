import numpy as np
import random
np.seterr(divide='ignore', invalid='ignore')



class Kmeans:
    def __init__(self, fname, n_clusters):
        self.n_clusters = n_clusters
        self.input_array = np.loadtxt(fname)
        self.label_array = np.zeros(self.input_array.shape, int)
        self.center_array = np.array(random.sample(self.input_array.tolist(), n_clusters))
        self.distance_square_array = np.ones([self.input_array.shape[0], n_clusters])
        self.cost = []

    def kmeans(self):
        while True:
            self.compute_distance_square_all()
            self.update_label()
            new_centers = self.update_centers()
            if self.has_converged(new_centers):
                break
            self.center_array = new_centers
        self.cost = self.compute_cost()

    def result(self):
        print("Center was found by algorithm:")
        for center in self.center_array:
            for value in center:
                print(value, end=" ")
            print()
        print("Cost for this run:")
        print(sum(self.cost)/self.n_clusters)

    def compute_distance_square_all(self):
        i = 0
        for point in self.input_array:
            j = 0
            for center in self.center_array:
                self.distance_square_array[i][j] = self.compute_distance_square(point, center)
                j += 1
            i += 1

    def update_label(self):
        self.label_array = np.argmin(self.distance_square_array, axis=1)

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
            cost_list.append(sum(self.compute_distance_square(Xk[i], self.center_array[k]) for i in range(Xk.shape[0]))/Xk.shape[0])
        return cost_list

    def compute_distance_square(self, point1, point2):
        distance_square = 0
        for i in range(len(point1)):
            distance_square += (point1[i] - point2[i]) ** 2
        return distance_square



km = Kmeans("out.txt", 5)
km.kmeans()
km.result()