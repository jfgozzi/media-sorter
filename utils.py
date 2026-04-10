from PIL import Image
import imagehash


def isRepeat(f, og_photos):
    f.seek(0)
    hashes = []
    im = Image.open(f)
    res = False
    for angulo in [0, 90, 180, 270]:
        im_rotada = im.rotate(angulo, expand=True)
        actualHash = str(imagehash.phash(im_rotada))
        res = res or (actualHash in og_photos)
    return res
