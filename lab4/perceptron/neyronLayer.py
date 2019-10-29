class NeyronLayer:
    def __init__(self, hideLayer, outLayer):
        self.hideLayer = hideLayer
        self.outLayer = outLayer

    def test_shape(self, test_shape):
        hideOut = []
        for hideNeyron in self.hideLayer:
            hideOut.append(hideNeyron.test_shape(test_shape))
        outOut = []
        for outNeyron in self.outLayer:
            outOut.append(outNeyron.test_shape(hideOut))
        return outOut
