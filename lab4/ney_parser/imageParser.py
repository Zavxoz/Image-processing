from PIL import Image, ImageDraw


def parse_image_to_shape(input_file):
    image = Image.open(input_file)  
    width = image.size[0]  
    height = image.size[1]  
    result = []
    for i in range(0, height):
        for j in range(0, width):
            if image.getpixel((i,j)) == 0:
                result.append(1)
            elif image.getpixel((i,j)) == 255:
                result.append(-1)
    return result
