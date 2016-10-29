from PIL import Image, ImageOps

def pil_adprocess(ad):

    ad = ImageOps.expand(ad, border=5, fill='black')
    bg = Image.new("RGB", (640, 480), "white")

    bg_w, bg_h = bg.size
    img_w, img_h = ad.size
    offset = ((bg_w - img_w) / 2, (bg_h - img_h) / 2)

    bg.paste(ad, offset)

    return bg
