import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from time import time
import urllib
from scipy.fftpack import dct, idct


def
X_kl = dct(dct(x_mn.T, norm='ortho').T , norm='ortho')
x_mn = idct(idct(X_kl.T, norm='ortho').T , norm='ortho')