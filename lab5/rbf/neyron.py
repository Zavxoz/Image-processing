class Neyron:
    def __init__(self, __weights: list, __restriction: float):
        self.__weights = None
        self.__size = None
        self.__restriction = None
        self.refresh(__weights, __restriction)

    def test_shape(self, __x_list: list) -> float:
        assert len(__x_list) == self.__size
        return sum([__x_list[i] * self.__weights[i] for i in range(0, self.__size)])

    def refresh(self, __weights: list, __restriction: float):
        self.__weights = __weights
        self.__size = len(__weights)
        self.__restriction = __restriction
