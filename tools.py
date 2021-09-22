import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import matplotlib.colors as colors
import matplotlib as mpl
import matplotlib.animation as animation



class Disease:

    def __init__(self, N, dead, probdead):
        self.N = N
        self.deadtime = dead
        self.prob_dead = probdead

    def initial(self, vac):
        X = np.zeros((self.N, self.N))
        k=0
        for i in tqdm(range(self.N)):
            for j in range(self.N):
                x = np.random.random()
                if x < vac:
                    #print("Normal")
                    X[i, j] = 2
                else:
                    #print("Vac")
                    X[i, j] = 1
        return X

    def neightbour_inside(self, X, i, j):
        Neix = []
        Neiy = []
        Nei = []

        mat = X[i-1:i+2, j-1:j+2]

        for k in range(mat.shape[0]):
            for l in range(mat.shape[1]):
                if (k, l) != (1, 1) :
                    Neix.append(i+k-1)
                    Neiy.append(j+l-1)
                    Nei.append(mat[k,l])

        return Nei, Neix, Neiy

    def place_first(self, X):
        x, y = np.random.randint(1, self.N-1, (1))[0], np.random.randint(1, self.N-1, (1))[0]
        print("Initial patient : ({},{})".format(x, y))
        X[x, y] = 3
        return X

    def update_loop(self, X, prob):

        tabX = []
        tabY = []

        for i in range(1, self.N-1):
            for j in range(1, self.N-1):
                #print(i, j)
                ind = X[i, j] == 3
                #print("ind = {}".format(ind))
                if ind:
                    #print(1)
                    Nei, Neix, Neiy = Disease(self.N, self.deadtime, self.prob_dead).neightbour_inside(X, i, j)
                    #print(Neix, Neiy, len(Nei))
                    for k in range(len(Nei)):
                        #print(k)
                        x = np.random.random()
                        if x < prob:
                            if X[Neix[k], Neiy[k]] == 1:
                                #print("Yes")
                                tabX.append(Neix[k])
                                tabY.append(Neiy[k])
        X[tabX, tabY] = 3

        return X

    def count(self, tab, X):
        ind = X == 3
        ind = np.where(ind == True)
        tab[ind[0], ind[1]] += 1
        return tab

    def transform_dead(self, count, X):
        ind = np.where(count > self.deadtime)
        #print(ind)
        x = np.random.random()

        if x < self.prob_dead:
            if len(ind[0]) != 0:
                X[ind[0], ind[1]] = 0
                count[ind[0], ind[1]] = 0
        else:
            X[ind[0], ind[1]] = 2

        return X, count

    def counting(self, X, time):

        tab_dead = np.zeros(time)
        tab_infected = np.zeros(time)
        tab_healty = np.zeros(time)

        for i in tqdm(range(time)):
            ind_0 = X[i] == 0
            ind_1 = X[i] == 1
            ind_3 = X[i] == 3

            ind_0 = np.sum(ind_0)
            ind_1 = np.sum(ind_1)
            ind_3 = np.sum(ind_3)

            tab_dead[i] = ind_0
            tab_infected[i] = ind_3
            tab_healty[i] = ind_1

        return tab_dead, tab_infected, tab_healty
