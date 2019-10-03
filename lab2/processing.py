import copy
import math

from PIL import Image, ImageDraw

INTENSITY_LAYER_NUMBER = 256 

def minimum(pix, i, j, k):
    tmp = [pix[i, j][k],
               pix[i + 1, j][k],
               pix[i, j + 1][k],
               pix[i + 1, j + 1][k],
               pix[i, j + 2][k],
               pix[i + 1, j + 2][k],
               pix[i + 2, j + 2 ][k],
               pix[i + 2, j + 1][k],
               pix[i + 2, j][k],
               pix[i + 3, j][k],
               pix[i, j + 3][k],
               pix[i + 1, j + 3][k],
               pix[i + 2, j + 3][k],
               pix[i + 3, j + 3][k],
               pix[i + 3, j][k],
               pix[i + 3, j + 1][k],
               pix[i + 3, j + 2][k],
               pix[i, j + 4][k],
               pix[i + 1, j + 4][k],
               pix[i + 2, j + 4][k],
               pix[i + 3, j + 4][k],
               pix[i + 4, j + 4][k],
               pix[i + 4, j][k],
               pix[i + 4, j + 1][k],
               pix[i + 4, j + 2][k],
               pix[i + 4, j + 3][k],]
    tmp.sort()
    return tmp[0]


def median(pix, i, j, k):
    import statistics
    return statistics.median((pix[i, j][k],
               pix[i + 1, j][k],
               pix[i, j + 1][k],
               pix[i - 1, j][k],
               pix[i, j - 1][k],
               pix[i + 1, j + 1][k],
               pix[i - 1, j + 1 ][k],
               pix[i - 1, j - 1][k],
               pix[i + 1, j - 1][k],
               pix[i + 2, j][k],
               pix[i, j + 2][k],
               pix[i - 2, j][k],
               pix[i, j - 2][k],
               pix[i + 2, j + 2][k],
               pix[i - 2, j + 2 ][k],
               pix[i - 2, j - 2][k],
               pix[i + 2, j - 2][k],
               pix[i + 1, j - 2][k],
               pix[i + 2, j - 1][k],
               pix[i + 2, j + 1][k],
               pix[i + 1, j + 2][k],
               pix[i - 1, j + 2][k],
               pix[i - 2, j + 1 ][k],
               pix[i - 2, j - 1][k],
               pix[i - 1, j - 2][k]))



def filtering(image):
    brush = ImageDraw.Draw(image)    
    pix = image.load()
    
    for i in range(image.width):
            for j in range(image.height):
                image.putpixel((i,j), tuple([round(0.9 * (image.getpixel((i,j))[k]/255) ** (2)*255)  for k in range(3)]))
    
    
    for i in range(image.size[0] - 4):
        for j in range(image.size[1] - 4):
            brush.point((i, j), fill=(
                minimum(pix, i, j, 0),
                minimum(pix, i, j, 1),
                minimum(pix, i, j, 2)))

    for i in range(2, image.size[0] - 2):
        for j in range(2, image.size[1] - 2):
            brush.point((i, j), fill=(
                median(pix, i, j, 0),
                median(pix, i, j, 1),
                median(pix, i, j, 2)))
            
    del brush
    image.show()
    
    return image


def otsuThreshold(img) :
    b = img.load()
    hist = [0 for i in range(256)]
    intens_sum = 0
    for j in range(img.height):
        for i in range(img.width):
            intens = int(b[i,j][0]*0.2126+b[i,j][1]*0.7152+b[i, j][2]*0.0722)
            intens_sum += intens
            hist[intens] += 1
    
    
    best_thresh = 0 
    best_sigma = 0.0 
    all_pixel_count = img.height * img.width
    first_class_pixel_count = 0 
    first_class_intensity_sum = 0 

    # Перебираем границу между классами
    # thresh < INTENSITY_LAYER_NUMBER - 1, т.к. при 255 в ноль уходит знаменатель внутри for
    for thresh in range(1, INTENSITY_LAYER_NUMBER):
        
        first_class_pixel_count += hist[thresh] 
        first_class_intensity_sum += thresh * hist[thresh] 

        first_class_prob = first_class_pixel_count / all_pixel_count 
        second_class_prob = 1.0 - first_class_prob 
        if first_class_pixel_count==0 or all_pixel_count - first_class_pixel_count == 0:
            continue
        first_class_mean = first_class_intensity_sum / first_class_pixel_count
        second_class_mean = (intens_sum - first_class_intensity_sum) / (all_pixel_count - first_class_pixel_count) 

        mean_delta = first_class_mean - second_class_mean 

        sigma = first_class_prob * second_class_prob * mean_delta * mean_delta 

        if (sigma > best_sigma) :
            best_sigma = sigma 
            best_thresh = thresh    
    
    array = []
    for j in range(img.height):
        for i in range(img.width):
            intens = int(b[i,j][0]*0.2126+b[i,j][1]*0.7152+b[i, j][2]*0.0722)
            if intens > best_thresh:
                x = (255, 255, 255)
            else:
                x = 0
            array.append(x)
            
    img.putdata(array)
    img = img.convert('L')
    return img 