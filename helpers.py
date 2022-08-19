import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

from PIL import Image, ImageFilter, ImageEnhance


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def enhancement(filter_name):
    image = Image.open('static/uploads/out.jpg')
    if filter_name == 'color':
        enhancer = ImageEnhance.Color(image)
    enhancer.enhance(0.9).save('static/uploads/result.jpg')


def noise_reduction():
    import matplotlib
    import numpy as np
    import matplotlib.pyplot as plt
    from skimage import data, img_as_float
    from skimage.restoration import denoise_nl_means, estimate_sigma
    from skimage.metrics import peak_signal_noise_ratio
    from skimage.util import random_noise
    original = Image.open("static/uploads/out.jpg")
    astro = img_as_float(original)

    sigma = 0.08
    noisy = random_noise(astro, var=sigma**2)
    sigma_est = np.mean(estimate_sigma(noisy, multichannel=True))
    patch_kw = dict(patch_size=5,
                patch_distance=6,
                multichannel=True)
    denoise_fast = denoise_nl_means(noisy, h=0.8 * sigma_est, fast_mode=True,
                                **patch_kw)
    matplotlib.pyplot.imsave("static/uploads/result.jpg", denoise_fast)

def filters(filter_name):
    image = Image.open('static/uploads/out.jpg')
    if filter_name == 'blur':
        result = image.filter(ImageFilter.BLUR)
    elif filter_name == 'contour':
        result = image.filter(ImageFilter.CONTOUR)
    elif filter_name == 'detail':
        result = image.filter(ImageFilter.DETAIL)
    elif filter_name == 'edge_enhance':
        result = image.filter(ImageFilter.EDGE_ENHANCE)
    elif filter_name == 'edge_enhance_more':
        result = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    elif filter_name == 'emboss':
        result = image.filter(ImageFilter.EMBOSS)
    elif filter_name == 'find_edges':
        result = image.filter(ImageFilter.FIND_EDGES)
    elif filter_name == 'sharpen':
        result = image.filter(ImageFilter.SHARPEN)
    elif filter_name == 'smooth':
        result = image.filter(ImageFilter.SMOOTH)
    elif filter_name == 'smooth_more':
        result = image.filter(ImageFilter.SMOOTH_MORE)

    result.save('static/uploads/result.jpg')


def sketch(value):
    def dodge(front,back):
        result=front*255/(255-back)
        result[result>255]=255
        result[back==255]=255
        return result.astype('uint8')
    import numpy as np
    def grayscale(rgb):
        return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
    img = value
    import imageio
    s = imageio.imread(img)
    g=grayscale(s)
    i = 255-g
    import scipy.ndimage
    b = scipy.ndimage.filters.gaussian_filter(i,sigma=10)
    r = dodge(b,g)
    import matplotlib.pyplot as plt
    plt.imsave('static/uploads/result.jpg', r, cmap='gray', vmin=0, vmax=255)
    return 0


def image_save(value):
    url = value
    import requests

    r = requests.get(url)
    print(r, type(r))
    print(r.status_code)

    if r.status_code != 200:
        return "Invalid URL or unsupported file format"

    import imageio
    s = imageio.imread(url)

    import matplotlib.pyplot as plt
    plt.imsave('static/uploads/out.jpg', s)