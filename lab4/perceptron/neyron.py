import math


class Neyron:
    def __init__(self, weights, restriction):
        self.weights = None
        self.size = None
        self.restriction = None
        self.refresh(weights, restriction)

    def activation(self, x):
        under = 1 + math.exp(-x)
        return 1 / float(under)

    def test_shape(self, x_list):
        if not (len(x_list) == self.size):
            print(x_list)
        assert len(x_list) == self.size
        return self.activation(sum([x_list[i] * self.weights[i] for i in range(0, self.size)]) + self.restriction)

    def refresh(self, weights, restriction):
        self.weights = weights
        self.size = len(weights)
        self.restriction = restriction

