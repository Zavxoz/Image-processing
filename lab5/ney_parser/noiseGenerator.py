import random as rnd

from PIL import Image, ImageDraw

PARSE1 = (0, 0, 0)
PARSE_1 = (255, 255, 255)


def to_tuple(__cur, __width, __height) -> tuple:
    i = __cur // __width
    j = __cur % __width
    return j, i


def gen_noise(__input_image: str, __output_image: str, __percent: int):
    image = Image.open(__input_image)  # Открываем изображение.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    imageOut = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(imageOut)  # Создаем инструмент для рисования.

    pix = image.load()  # Выгружаем значения пикселей.
    for i in range(height):
        for j in range(width):
            draw.point((j, i), pix[j, i])

    used = []
    cur = 0
    length = (width * height)
    count = length * float(__percent / float(100))

    while len(used) < count:
        if cur >= length:
            cur = 0
        index = to_tuple(cur, width, height)
        if index not in used:
            choice = bool(rnd.getrandbits(1))
            if choice:
                if pix[index] == PARSE1:
                    draw.point(index, PARSE_1)
                if pix[index] == PARSE_1:
                    draw.point(index, PARSE1)
                used.append(index)
        cur += 1
    imageOut.save(__output_image, "PNG")