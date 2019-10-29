from ney_parser import imageParser as imp
from ney_parser import noiseGenerator as ng
from perceptron import neyronLayerBuilder


def generate_noise(__original, __count, __noises):
    shapes = []
    for origin in __original:
        for i in __noises:
            outGen = "./images_with_noise/"+origin.rsplit(".")[1].split("/")[-1] + "_" + str(i) + "_"
            for j in range(0, __count):
                ng.gen_noise(origin, outGen + str(j) + ".png", i)
                shapes.append(outGen + str(j) + ".png")
    return shapes


if __name__ == "__main__":
    N = 36
    H = 10
    M = 5

    ALPHA = 0.5
    BETA = 0.5
    D = 0.008

    learnShapesFiles = ["./patterns/" + str(i) + ".png" for i in range(0, 5)]
    noises = [5, 10, 15]
    count = 1

    learnShapesY = [
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1]
    ]

    testShapesFiles = generate_noise(learnShapesFiles, count, noises)
    teachShapes = []

    for fileName in learnShapesFiles:
        shape = imp.parse_image_to_shape(fileName)
        teachShapes.append(shape)
    builder = NeyronLayerBuilder(N, H, M)
    builder.randomInit(-1, 1)

    for _ in range(5):
        for i in range(0, len(teachShapes)):
            builder.teach(teachShapes[i], learnShapesY[i], ALPHA, BETA, D)

    layerNetwork = builder.build()

    for test in testShapesFiles:
        print(test)
        print(layerNetwork.test_shape(imp.parse_image_to_shape(test)))

