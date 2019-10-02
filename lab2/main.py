from processing import otsuThreshold, filtering
from detect import ImageObjectDetector
from PIL import Image


def main():
    image = Image.open('b.jpg')
    image.show()
    image = otsuThreshold(filtering(image))
    image.show()
    detector = ImageObjectDetector(image)
    detector._labeling()
    
    detector._kmedians()
    detector._colorize_clusters()
    detector._show()


if __name__ == "__main__":
    main()
