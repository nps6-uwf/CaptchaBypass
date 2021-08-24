# A collection of image preprocessing techniques.
# Author: NS
#


import numpy as np
import cv2
from string import punctuation, ascii_uppercase as ABC, digits
punctuation += '—' # non ascii — symbol character, manually adding.


def get_grayscale(image):
    '''Convert image to grayscale.
    '''
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def remove_noise(image):
    '''Remove noise using the median blur technique.
    '''
    return cv2.medianBlur(image,5)


def thresholding(image):
    ''' Use thresholding.
    '''
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def dilate(image):
    '''Dilate
    '''
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)


def erode(image):
    '''Erosion
    '''
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)


def opening(image):
    '''Opening - erosion followed by dilation
    '''
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)



def canny(image):
    '''Canny edge detection.
    '''
    return cv2.Canny(image, 100, 200)


def deskew(image):
    '''skew correction
    '''
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def replace_punctuation(s: str) -> str:
    '''Replace all punctuation characters from a string.
    '''
    for symbol in punctuation: 
        s = s.replace(symbol, "")
    return s

def apply_all(image, gs=True, rm=True, ts=True,
    di = True, er = True, cn = True, op = True, ds = True):
    '''grayscale: convert image to grayscale,
    di = dilate
    er = erode
    op = openess
    ds = deskew
    '''
    if gs: image = get_grayscale(image)
    if rm: image = remove_noise(image)
    if ts: image = thresholding(image)
    if di: image = dilate(image)
    if er: image = erode(image)
    if cn: image = canny(image)
    if op: image = opening(image)
    if False: image = deskew(image)

    return image