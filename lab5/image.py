import random
import imageio
import glob
import numpy as np
import os
from PIL import Image

def img2bin(input_file):
    image = Image.open(input_file)  
    width = image.size[0]  
    height = image.size[1]  
    result = []
    for i in range(0, height):
        for j in range(0, width):
            if image.getpixel((i,j)) == 0:
                result.append(1)
            elif image.getpixel((i,j)) == 255:
                result.append(0)
    return result


def diff(pattern, img):
    k = 0
    for i in range(pattern.shape[0]):
        for j in range(pattern.shape[1]):
            if pattern[i, j] == img[i, j]:
                k += 1
    return (pattern.size - k) * 100 / (pattern.shape[0] * pattern.shape[1])


def noise_generator(img, percent):
    res = np.array(img).copy()
    num = percent * img.size // 100
    loc = random.sample(range(img.size), num)
    xy = [(i // img.shape[0], i % img.shape[1]) for i in loc]
    for i in xy:
        res[i] = 1 if img[i] == 0 else 0
    return res

def show(img):
    print('\n'.join(''.join('X' if cell == 0 else ' ' for cell in row) for row in img))
