import random as rnd

from rbf.neyron import Neyron
from rbf.neyronLayer import NeyronLayer
from rbf.rbfNeyron import RBFNeyron


class NeyronLayerBuilder:
    def __init__(self, __n_size: int, __h_size: int, __m_size: int, __sigma: float):
        self.__n_size = __n_size
        self.__h_size = __h_size
        self.__m_size = __m_size
        self.__sigma = __sigma

        """Hide matrix NxH"""
        self.__RBFMatrix = None
        """Out matrix HxM"""
        self.__OutMatrix = None

        self.__RBFRestriction = None
        self.__OutRestriction = None

        self.__RBFNeyrons = None
        self.__outNeyrons = None

    def randomInit(self, __start: float, __stop: float):
        self.__RBFMatrix = [[rnd.uniform(__start, __stop) for _ in range(0, self.__h_size)] for _ in
                            range(0, self.__n_size)]
        self.__OutMatrix = [[rnd.uniform(__start, __stop) for _ in range(0, self.__m_size)] for _ in
                            range(0, self.__h_size)]

        self.__RBFRestriction = [rnd.uniform(__start, __stop) for _ in range(0, self.__h_size)]
        self.__OutRestriction = [rnd.uniform(__start, __stop) for _ in range(0, self.__m_size)]

        rbf_t = list(zip(*self.__RBFMatrix))
        self.__RBFNeyrons = [
            RBFNeyron(list(rbf_t[i]), self.__RBFRestriction[i], self.__sigma) for i in
            range(0, self.__h_size)]
        out_t = list(zip(*self.__OutMatrix))
        self.__outNeyrons = [Neyron(list(out_t[i]), self.__OutRestriction[i]) for i in range(0, self.__m_size)]

    def init_centres(self, __centers: list):
        print(len(__centers), len(self.__RBFNeyrons))
        assert len(__centers) == len(self.__RBFNeyrons)
        for i in range(len(__centers)):
            self.__RBFNeyrons[i].refresh_t_vector(__centers[i])

    def teach(self, __shape: list, __out: list, __alpha: float, __beta: float, __D: float):
        flagStart = True
        MAX_DK = 0
        countTeach = 0
        while (MAX_DK >= __D) or flagStart:
            MAX_DK = 0
            flagStart = False
            rbfOut = []
            for rbfNeyron in self.__RBFNeyrons:
                rbfOut.append(rbfNeyron.test_shape(__shape))
            outOut = []
            for outNeyron in self.__outNeyrons:
                outOut.append(outNeyron.test_shape(rbfOut))

            # ---------------OUT-Layer---------------------
            for j in range(0, len(self.__OutMatrix)):
                for k in range(0, len(self.__OutMatrix[j])):
                    yk = outOut[k]
                    dk = __out[k] - yk
                    MAX_DK = max(MAX_DK, abs(dk))
                    temp = __alpha * dk
                    self.__OutMatrix[j][k] += temp * rbfOut[j]

            out_t = list(zip(*self.__OutMatrix))
            for i in range(0, self.__m_size):
                self.__outNeyrons[i].refresh(list(out_t[i]), self.__OutRestriction[i])
            countTeach += 1
        print("TEACH WAS COMPLETE = " + str(countTeach))

    def build(self) -> NeyronLayer:
        return NeyronLayer(self.__RBFNeyrons, self.__outNeyrons)


def generate(__x: int, __length: int):
    return [1 if (i == __x) else 0 for i in range(0, __length)]
