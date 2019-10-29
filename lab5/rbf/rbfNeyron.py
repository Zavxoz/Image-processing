import math


class RBFNeyron:
    def __init__(self, __weights: list, __restriction: float, __sigma: float):
        self.__weights = None
        self.__size = None
        self.__restriction = None
        self.__t_vector = None
        self.__sigma = __sigma
        self.refresh(__weights, __restriction)

    def test_shape(self, __x_list: list) -> float:
        assert len(__x_list) == self.__size
        part = (-distance(__x_list, self.__t_vector)) / (float(self.__sigma ** 2))
        return math.exp(part)

    def refresh(self, __weights: list, __restriction: float):
        self.__weights = __weights
        self.__size = len(__weights)
        self.__restriction = __restriction

    def refresh_t_vector(self, __t_vector: list):
        self.__t_vector = __t_vector



def distance(__x: list, __y: list) -> float:
    assert len(__x) == len(__y)
    return sum([(__x[i] - __y[i]) ** 2 for i in range(0, min(len(__x), len(__y)))])
