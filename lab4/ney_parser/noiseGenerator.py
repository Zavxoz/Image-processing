import random as rnd
from PIL import Image, ImageDraw



def to_tuple(cur, width, height):
    i = cur // width
    j = cur % width
    return j, i


def gen_noise(input_image, output_image, percent):
    image = Image.open(input_image)  
    width = image.size[0] 
    height = image.size[1]
    imageOut = Image.new('L', (width, height))

    for i in range(height):
        for j in range(width):
            imageOut.putpixel((j, i), image.getpixel((j,i)))

    used = []
    cur = 0
    length = (width * height)
    count = length * float(percent / float(100))

    while len(used) < count:
        if cur >= length:
            cur = 0
        index = to_tuple(cur, width, height)
        if index not in used:
            choice = bool(rnd.getrandbits(1))
            if choice:
                if image.getpixel(index) == 0:
                    imageOut.putpixel(index, 255)
                if image.getpixel(index) == 255:
                    imageOut.putpixel(index, 0)
                used.append(index)
        cur += 1
    imageOut.save(output_image)