from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

def get_patch(shape, image):
    w,h,_ = image.shape
    dw, dh = shape

    x = np.random.randint(0, w - dw)
    y = np.random.randint(0, h - dh)

    return image[x:x+dw, y:y+dh]
