from PIL import Image, ImageDraw

PARSE1 = (0, 0, 0)
PARSE_1 = (255, 255, 255)


def parse_image_to_shape(__input_file: str) -> list:
    image = Image.open(__input_file)  # Открываем изображение.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.
    result = []
    for i in range(0, height):
        for j in range(0, width):
            if pix[j, i] == PARSE1:
                result.append(1)
            elif pix[j, i] == PARSE_1:
                result.append(-1)
    return result


def from_shape_to_image(__shape: list, __output_path: str, __size: int):
    assert len(__shape) == __size ** 2
    image = Image.new('RGB', (__size, __size))
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    cur = 0
    for i in range(__size):
        for j in range(__size):
            if __shape[cur] == 1:
                draw.point((j, i), PARSE1)
            elif __shape[cur] == -1:
                draw.point((j, i), PARSE_1)
            cur += 1
    image.save(__output_path, "PNG")