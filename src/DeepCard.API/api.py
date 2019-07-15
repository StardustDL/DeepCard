import traceback
from io import BytesIO
from PIL import Image
from ocr import ocr
import numpy as np
import json
import os

def validBegin(s):
    return s.startswith("62") or s.startswith("60") or s.startswith("34") or s.startswith("35") or s.startswith("37") or s.startswith("51") or s.startswith("52") or s.startswith("53") or s.startswith("54") or s.startswith("55") or s.startswith("9") or s.startswith("43") or s.startswith("48") or s.startswith("42")

def filterLong(results):
    res = ""
    for cs in results:
        trimed = "".join([c for c in cs if c.isdigit()])
        l = len(trimed) # 16-19
        if len(trimed) > len(res):
            res = trimed
    return res

def filter(results):
    res = ""
    for cs in results:
        trimed = "".join([c for c in cs if c.isdigit()])
        l = len(trimed) # 16-19
        if l < 16 or l > 19:
            continue
        while trimed != "" and not validBegin(trimed):
            trimed = trimed[1:]
        if len(trimed) == 0:
            continue
        if len(trimed) >= 19:
            trimed = trimed[0:19]
        elif len(trimed) >= 16:
            pass
        else:
            continue
        if len(trimed) > len(res):
            res = trimed
    return res if res != "" else filterLong(results)

def get_result(img):
    if os.getenv("IN_DEMO"):
        return "00000000000000000"
    image = np.array(img.convert('RGB'))
    result, _ = ocr(image)
    return filter(map(lambda x: x[1], result.values()))