# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 19:40:29 2020
@author: DIRK
"""
#%%
from path import Path
import os
import pylab as plt
import sys
import shutil

ww, hh =  16, 9
r = ww/hh


filepath = Path(sys.argv[1])
filepathout = Path(filepath+'__converted')
os.makedirs(filepathout, exist_ok=True)


#%%
for p in sorted(filepath.walk()):

    if p.isdir(): continue

    pout = Path(p.replace(filepath, filepathout))
    if p.splitext()[0].endswith("--converted"):
        shutil.copy(p, pout)
        continue

    pout = Path(pout.stripext()+"--converted"+pout.splitext()[-1])

    im = plt.imread(p)
    w, h, _ = im.shape

    w2, h2 = w, h

    print("")
    print(w/h)
    if w/h < r:
        h2 = int(round(w*r))
    else:
        w2 = int(round(h/r))


    wb = int(round((w2-w)/2))
    hb = int(round((h2-h)/2))

    print(f"{w}:{w2} <-> {h}:{h2}")

    imout = plt.zeros([w2, h2, im.shape[-1]], dtype=im.dtype)

    try:
        imout[wb:wb+w, hb:hb+h, :] = im

        plt.imsave(pout, imout)
    except:
        plt.imsave(pout, im)
        assert False