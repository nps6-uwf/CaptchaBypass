# Captcha Solving Service
# Author: Nick Sebasco
# Date: 8/23/2021
# Version: 0
# 


import pytesseract as pyt 
import cv2
import os
from img_utils import apply_all, replace_punctuation
from flask import Flask
app = Flask(__name__)


# Adding custom options: restrict whitelisted characterset to hopefully improve accuracy.
custom_config = r'-l eng -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --oem 3 --psm 6 '
optimal_params =  (False, True, False, False, False, False, False, False) # discovered in test2


@app.route('/<fileName>/<threshold>/<rmFile>')
def main(fileName = None, threshold = 1, rmFile = 0):
    '''Attempts to solve a captcha.
    Parameters:
    1) fileName: [str] path to captcha
    2) threshold: [float] confidence threshold
    3) rmFile: [int] integer (0 or 1) representing whether or not to delete the captcha image.
    '''
    try:
        threshold = float(threshold)
        print("->a")
        img = apply_all(cv2.imread(f"scaper/csImages/{fileName}.png"), *optimal_params)
        
        res0 = pyt.image_to_string(img, config=custom_config)
        print("->b")
        res = replace_punctuation(res0.upper().strip())
        results = pyt.image_to_data(img, output_type=pyt.Output.DICT, config=custom_config)

        if bool(int(rmFile)):
            os.remove(f"scaper/csImages/{fileName}.png")
        
        if results['conf'][-1] >= threshold:
            return res
        else:
            # Condidence to low to report result.
            return "None"

    except Exception:
        return "Proccessing error."


if __name__ == '__main__': app.run()