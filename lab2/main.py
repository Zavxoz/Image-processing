from processing import otsuThreshold, filtering
from detect import ImageObjectDetector
from PIL import Image


def main():
    image = Image.open('d.jpg')
    image.show()
    image = otsuThreshold(filtering(image))
    image.show()
    detector = ImageObjectDetector(image)
    detector.labeling()
    
    detector.kmedians()
    detector.colorize_clusters()
    detector.show()


if __name__ == "__main__":
    main()
