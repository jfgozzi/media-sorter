import sys
from PIL import Image

im = Image.open("lolo.JPG")
print(im.format, im.size, im.mode)


