
from image import *
from net import Concurrent_Net
import time
from PIL import Image

names = ["n.png","f.png", "i.png", "p.png", "d.png"]
if __name__ == '__main__':
    bin_images=[]
    for i in names:
        bin_images.append(img2bin(f"./images/{i}"))
    print(bin_images)
    net = Concurrent_Net(36, 5, 0.1)

    net.train(bin_images)

    for img in range(0,5):
        print('\n' + names[img] + ':')
        for j in range(1,4):
            winner = net.recognize(img2bin("./images_with_noise/"+str(img)+"_"+str(j*5)+"_0.png"))
            print('Recognized', names[winner], '-------- : ' + str(j*5) + '%')
