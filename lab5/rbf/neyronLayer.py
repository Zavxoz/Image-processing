class NeyronLayer:
    def __init__(self, __hideLayer: list, __outLayer: list):
        self.__hideLayer = __hideLayer
        self.__outLayer = __outLayer

    def test_shape(self, __test_shape: list) -> list:
        hideOut = []
        for hideNeyron in self.__hideLayer:
            hideOut.append(hideNeyron.test_shape(__test_shape))
        outOut = []
        for outNeyron in self.__outLayer:
            outOut.append(outNeyron.test_shape(hideOut))
        return outOut
