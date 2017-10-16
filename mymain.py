import random

#Ham nhap du lieu
def input_data(file_name):
    X = []
    with open(file_name) as fileobject:
        for line in fileobject:
            Xi = [float(n)for n in line.strip().split('\t')]
            X.append(Xi)
    return X




#Ham tao list dang ma tran nxm voi gia tri ban dau 0
def zeros(d, c):
    matrix = []
    for i in range(d):
        row = []
        for j in range(c):
            row.append(0)
        matrix.append(row)
    return matrix

#Ham tinh mean
def mean(cluster):
    clen = len(cluster)
    if clen == 0:
        return None
    center = []
    #print cluster
    for i in range(len(cluster[0])):
        avgi = 0
        for j in range(clen):
            avgi += cluster[j][i]
        avgi /= clen
        center.append(avgi)
    return center

#Ham tinh binh phuong khoang cach giua 2 diem
def distance_two_points_square(pA, pB):
    if len(pA) != len(pB):
        print '2 Vector khong cung do dai'
        pass
    dist_sqr = 0
    for i in range(len(pA)):
        dist_sqr += (pA[i]-pB[i])*(pA[i]-pB[i])
    return dist_sqr

def collection_dist_sqr(centers, X):
    collection_dist = []
    for i in range(len(X)):
        list_dist = [] #khaong cach tu mot diem toi tung center
        for j in range(len(centers)):
            list_dist.append(distance_two_points_square(centers[j], X[i]))
        collection_dist.append(list_dist)
    return collection_dist


def kmeans_init_centers(X, k):
    # randomly pick k rows of X as initial centers
    lenX = len(X)
    centers = random.sample(X, 5)
    return centers




def kmeans_assign_labels(X, centers):
    # calculate pairwise distances btw data and centers
    D = collection_dist_sqr(centers, X)
    argmin = []

    for i in range(len(D)):
        argmin.append(D[i].index(min(D[i])))
        # return index of the closest center
    return argmin


def kmeans_update_centers(X, labels, K, oldcenters):
    ncenters = zeros(K, len(X[0]))
    for k in range(K):
        # collect all points assigned to the k-th cluster:
        Xk = []
        for i in range(len(X)):
            if labels[i] == k:
                Xk.append(X[i])
        # take average
        if mean(Xk) != None:
            ncenters[k] = mean(Xk)
        else:
            ncenters[k] = oldcenters[k]
    return ncenters

def has_converged(centers, new_centers):
    # return True if two sets of centers are the same
    return (set([tuple(a) for a in centers]) ==
        set([tuple(a) for a in new_centers]))

def ouput_to_excel(X, labels, centers):
    import xlwt

    wb = xlwt.Workbook()
    ws = []
    rowindex = []
    for i in range(len(centers)):
        ws.append(wb.add_sheet("My Sheet"+ " " +str(i)))
        rowindex.append(0)
    for i, row in enumerate(X):
        for j, col in enumerate(row):
            ws[labels[i]].write(rowindex[labels[i]], j, col)
        rowindex[labels[i]]+=1
    wb.save("data_out.xls")

def calc_avg_dist_by_labels(X, labels, centers):
    sum_distance = []
    cluster_len = []
    for i in range(len(centers)):
        sum_distance.append(0)
        cluster_len.append(0)


    for i in range(len(X)):
        sum_distance[labels[i]] += distance_two_points_square(X[i], centers[labels[i]])
        cluster_len[labels[i]] += 1

    avg_dist = []
    for i in range(len(centers)):
        if cluster_len[i] == 0:
            avg_dist.append(sum_distance[i])
        else:
            avg_dist.append(sum_distance[i]/cluster_len[i])
    return sum(avg_dist)/len(centers)


def kmeans(X, K= 5):
    centers = kmeans_init_centers(X, K)
    labels = []
    it = 0
    while True:
        labels = kmeans_assign_labels(X, centers)
        new_centers = kmeans_update_centers(X, labels, K, centers)
        if has_converged(centers, new_centers):
            break
        centers = new_centers
        it += 1

    return (centers, labels, it, calc_avg_dist_by_labels(X, labels, centers))


# gX = input_data('out.txt')
#
# (gcenters, glabels, git) = kmeans(gX, 5)
#
# print 'Center of each clusters found by algorithm:'
# for i in range (len(gcenters)):
#     print gcenters[i]

def loop_100_kmeans(X, K = 5):
    results = []
    for i in range(100):
        results.append(kmeans(X, K))
    index_min = 0
    for i in range(100):
        if(results[index_min][3] > results[i][3]):
            index_min = i
    print results[i][3]
    ouput_to_excel(X, results[i][1], results[i][0])
    return [results[i][0], results[i][1], results[i][2]]





