import random as rnd

from perceptron.neyron import Neyron
from perceptron.neyronLayer import NeyronLayer


class NeyronLayerBuilder:
    def __init__(self, n_size, h_size, m_size):
        self.n_size = n_size
        self.h_size = h_size
        self.m_size = m_size
        """Hide matrix NxH"""
        self.HideMatrix = None
        """Out matrix HxM"""
        self.OutMatrix = None

        self.HideRestriction = None
        self.OutRestriction = None

        self.hideNeyrons = None
        self.outNeyrons = None

    def randomInit(self, start, stop):
        self.HideMatrix = [[rnd.uniform(start, stop) for _ in range(0, self.h_size)] for _ in
                             range(0, self.n_size)]
        self.OutMatrix = [[rnd.uniform(start, stop) for _ in range(0, self.m_size)] for _ in
                            range(0, self.h_size)]

        self.HideRestriction = [rnd.uniform(start, stop) for _ in range(0, self.h_size)]
        self.OutRestriction = [rnd.uniform(start, stop) for _ in range(0, self.m_size)]

        hide_t = list(zip(*self.HideMatrix))
        self.hideNeyrons = [Neyron(list(hide_t[i]), self.HideRestriction[i]) for i in
                              range(0, self.h_size)]
        out_t = list(zip(*self.OutMatrix))
        self.outNeyrons = [Neyron(list(out_t[i]), self.OutRestriction[i]) for i in range(0, self.m_size)]

    def teach(self, shape, out, alpha, beta, D):
        flagStart = True
        MAX_DK = 0
        countTeach = 0
        while (MAX_DK >= D) or flagStart:
            MAX_DK = 0
            flagStart = False
            hideOut = []
            for hideNeyron in self.hideNeyrons:
                hideOut.append(hideNeyron.test_shape(shape))
            outOut = []
            for outNeyron in self.outNeyrons:
                outOut.append(outNeyron.test_shape(hideOut))

            # ---------------OUT-Layer---------------------
            for j in range(0, len(self.OutMatrix)):
                for k in range(0, len(self.OutMatrix[j])):
                    yk = outOut[k]
                    dk = out[k] - yk
                    MAX_DK = max(MAX_DK, abs(dk))
                    temp = alpha * yk * (1 - yk) * dk
                    self.OutMatrix[j][k] += temp * hideOut[j]
                    if j == 0:
                        self.OutRestriction[k] += temp

            # ---------------HIDE-Layer---------------
            for i in range(0, len(self.HideMatrix)):
                for j in range(0, len(self.HideMatrix[i])):
                    ej = 0
                    for k in range(0, len(outOut)):
                        yk = outOut[k]
                        dk = out[k] - yk
                        MAX_DK = max(MAX_DK, abs(dk))
                        proizv = yk * (1 - yk)
                        ej += dk * proizv * self.OutMatrix[j][k]
                    gj = hideOut[j]
                    temp = beta * gj * (1 - gj) * ej
                    self.HideMatrix[i][j] += temp * shape[i]
                    if i == 0:
                        self.HideRestriction[j] += temp

            out_t = list(zip(*self.OutMatrix))
            for i in range(0, self.m_size):
                self.outNeyrons[i].refresh(list(out_t[i]), self.OutRestriction[i])
            hide_t = list(zip(*self.HideMatrix))
            for i in range(0, self.h_size):
                self.hideNeyrons[i].refresh(list(hide_t[i]), self.HideRestriction[i])
            countTeach += 1
        print("Количество шагов = " + str(countTeach))

    def build(self):
        return NeyronLayer(self.hideNeyrons, self.outNeyrons)
