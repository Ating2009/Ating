
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


def convert_img(img,threshold):
    img = img.convert("L")  # 处理灰度
    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):
            if pixels[x, y] > threshold:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return img


captcha = Image.open("C:/Users/Administrator/Desktop/pycharm/yzm/7.png")
convert_img(captcha,150)
result = pytesseract.image_to_string(captcha)
print(result)