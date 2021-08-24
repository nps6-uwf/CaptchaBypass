# Bypassing poorly designed captchas, with OCR.
# This file run several experiements:
# 1) test2: find optimal set of preprocessing parameters, minimize leveshtein distance.
# 2) test3/4: find optimal ocr confidence, and perform a character analysis to determine characters that are typically read wrong.
# Author: Nick Sebasco
# Date: 8/21


import pytesseract as pyt 
import cv2
from os import listdir
import numpy as np
from img_utils import apply_all, replace_punctuation
import pickle


def binCombos(n: int = 8) -> list:
    '''Generate all permutations of n true/ false arguments to be supplied to a function.
    Motivation: Let each bit in a binary string represent the boolean value true or false.  Then given 
    n boolean parameters, we can generate all combinations of these parameters by counting to the largest 
    n-bit binary number in binary.   
    '''
    binStrings = [bin(i).replace("0b","").zfill(n) for i in range(sum([2 ** i for i in range(n)])+1)]
    return [tuple([bool(int(i)) for i in arg]) for arg in binStrings]


def levenshtein(s1: str, s2: str) -> np.matrix:
    '''AKA: Edit distance
    levenshtein distance between two sequences s1, s2 is the minimum number of single
    element (insert/ delete/ substitution) required to transform s1 -> s2.
    '''
    # 1. initialize matrix
    T = np.zeros((len(s1) + 1, len(s2) + 1))
    for i in range(max(len(s1)+1, len(s2)+1)):
        if i < len(s1)+1:
            T[i, 0] = i
        if i < len(s2)+1:
            T[0, i] = i
    # 2. 
    for i in range(len(s1)):
        for j in range(len(s2)):
            T[i + 1, j + 1] = min(T[i, j + 1], T[i + 1, j], T[i, j]) + 1 if s1[i] != s2[j] else T[i, j]

    return T


def test0():
    imgName = "1wzfn6"
    img = cv2.imread(f'captchas/{imgName}.png')
    img = apply_all(img, gs=True, rm=True, ts=True, di=True, er=True, cn=True, op=True, ds=True)

    # Adding custom options
    custom_config = r'--oem 3 --psm 6'
    print(
        pyt.image_to_string(img, config=custom_config)
    )


def test1():
    combos = binCombos()[:15]
    imgName = "1wzfn6".upper()
    # Adding custom options: restrict whitelisted characterset to hopefully improve accuracy.
    custom_config = r'-l eng -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --oem 3 --psm 6 '
    for i, j in enumerate(combos):
        print(f"test {i}", j)

        img = cv2.imread(f'captchas/{imgName}.png')
        img = apply_all(img, *j)

        
        res = replace_punctuation(pyt.image_to_string(img, config=custom_config))
        res = res.upper()
        print("result: ", res)


def test2():
    ''' Use binCombos to generate all possible combinations of the parameters to apply_all.  The goal here 
    is to find the "optimal" set of image pre-processing parameters that minimize the levenshtein distance between 
    OCR output and actual captcha string.

    Results:
    Examine the confidence of each OCR reading if it is greater than some threshold value, strip out the non alphanumeric
    characters and ensure the string length is 6; then conclude that the captcha was correctly read.

    Optimal parameters:  (False, True, False, False, False, False, False, False) -> the only necessary pre-processing is noise removal.
    Minimum total Levenschtein distance:  19.0
    '''
    min_dist, min_parameter_set = float("inf"), None

    # Adding custom options
    custom_config = r'--oem 3 --psm 6'
    # Adding custom options: restrict whitelisted characterset to hopefully improve accuracy.
    custom_config = r'-l eng -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --oem 3 --psm 6 '
    for i, j in enumerate(binCombos()):
        print(f"test {i}", j)

        success = True
        total_dist = 0
        for imgName in listdir('testImages'):
            try: 
                img = cv2.imread(f'testImages/{imgName}')
                imgName = imgName.upper().strip().replace('.PNG','')
                img = apply_all(img, *j)

                res = replace_punctuation(pyt.image_to_string(img, config=custom_config))
                res = res.upper().strip()
                dist = levenshtein(res, imgName)
                total_dist += dist[dist.shape[0]-1, dist.shape[1]-1]
                results = pyt.image_to_data(img, output_type=pyt.Output.DICT, config=custom_config)
                print(res, imgName)
                print("confidence: ", results['conf'][-1])
            except Exception:
                success = False
                print("Error: ",j)

        if success:
            if total_dist < min_dist:
                min_dist = total_dist
                min_parameter_set = j

            print("total distance: ",total_dist)
            print()           


    print("Optimal parameters: ", min_parameter_set)
    print("Minimum total Levenschtein distance: ", min_dist)


def test3():
    '''Examine confidence level for every correctly solved captcha.

    Results:
    2/3 of the images with a confidence thresold set at 50, were solved correctly.  There was approximately a 12% chance of
    solving a captcha and meeting the confidence threshold.  Test 4 will investigate the distribution of errors.
    '''
    # Adding custom options: restrict whitelisted characterset to hopefully improve accuracy.
    custom_config = r'-l eng -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --oem 3 --psm 6 '
    optimal_params =  (False, True, False, False, False, False, False, False) # discovered in test2

    N = len(listdir('testImages'))
    totalCorrect = 0

    totalConfident = 0
    confidentCorrect = 0
    thresholdConfidence = 50

    for imgName in listdir('testImages'):
        try: 
            
            img = cv2.imread(f'testImages/{imgName}')
            imgName = imgName.upper().strip().replace('.PNG','')
            img = apply_all(img, *optimal_params)
            
            res0 = pyt.image_to_string(img, config=custom_config)
            res = replace_punctuation(res0.upper().strip())
            # dist = levenshtein(res, imgName)
            results = pyt.image_to_data(img, output_type=pyt.Output.DICT, config=custom_config)
            print(res0, res, imgName)
            print("confidence: ", results['conf'][-1])

            if res == imgName:
                totalCorrect += 1

            if results['conf'][-1]> thresholdConfidence:
                totalConfident += 1
                if res == imgName:
                    confidentCorrect += 1

        except Exception:
            print("Error: ", imgName)
    
    print()
    print(f"Total images processed: {N}")
    print(f"Overall correct: {100 * totalCorrect/ N: 0.2f}%")
    print(f"Results exceeding confidence threshold: {totalConfident}/ {N}.  Percentage correct: {100 * confidentCorrect/ totalConfident:0.2f}%")
    return None


def test4():
    '''Examine the errors made when attempting to solve the captcha.
    Results:
        Data plotted via plot.py:
            High Error Rates:
                E
                I
                O
                S
                0

            Most Accurate:
                H
                N
                7
                D
    '''
    # Adding custom options: restrict whitelisted characterset to hopefully improve accuracy.
    custom_config = r'-l eng -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --oem 3 --psm 6 '
    optimal_params =  (False, True, False, False, False, False, False, False) # discovered in test2

    # data
    data = {

        "length_not_match": 0, # how many times the string lengths do not match.
        "character": {i: {"correct": 0, "incorrect": []} for i in (ABC + digits)}
    }

    for imgName in listdir('testImages'):
        try: 
            
            img = cv2.imread(f'testImages/{imgName}')
            imgName = imgName.upper().strip().replace('.PNG','')
            img = apply_all(img, *optimal_params)
            
            res0 = pyt.image_to_string(img, config=custom_config)
            res = replace_punctuation(res0.upper().strip())
            # dist = levenshtein(res, imgName)
            results = pyt.image_to_data(img, output_type=pyt.Output.DICT, config=custom_config)
            print(res0, res, imgName)
            print("confidence: ", results['conf'][-1])

            if res != imgName:
                if len(res) != len(imgName):
                    data["length_not_match"] += 1
                else:
                    for i, j in zip(res, imgName):
                        if i == j:
                            data["character"][i]["correct"] += 1
                        else:
                            data["character"][i]["incorrect"].append(j)
                            # data["character"][j]["incorrect"].append(i) # optionally enable this (observe error both ways).

        except Exception:
            print("Error: ", imgName)
    
    print()
    print(f"Total images processed: {len(listdir('testImages'))}")
    print(data)

    # creates a pickled data object which can be consumed and transformed into charts by visualizations/plot.py
    with open("captchaDataRes.pickle", "wb") as fobj:
        pickle.dump(data, fobj)

    return None

if __name__ == "__main__": test4()



