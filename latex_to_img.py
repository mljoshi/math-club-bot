import matplotlib.pyplot as plt
import io
from PIL import Image, ImageChops

white = (255, 255, 255, 255)

def latex_to_img(tex):
    buf = io.BytesIO()
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.axis('off')
    plt.text(0, 0.95, f'${tex}$', size=20, wrap=True)
    plt.savefig(buf, format='png')
    plt.close()

    im = Image.open(buf)
    return im
    bg = Image.new(im.mode, im.size, white)
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    return im.crop(bbox)

#latex_to_img(r'\frac{x}{y^2}').save('img.png') # this saves to C:\Users\Joshi for some reason