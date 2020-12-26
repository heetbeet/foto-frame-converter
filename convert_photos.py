from path import Path
import os
import pylab as plt
import numpy as np
import sys
import shutil

hh, ww = 9, 16


filepath = Path(sys.argv[1])
filepathout = Path(filepath+'__converted')
os.makedirs(filepathout, exist_ok=True)


for p in sorted(filepath.walk()):

    if p.isdir(): continue

    pout = Path(p.replace(filepath, filepathout))
    if p.splitext()[0].endswith("--converted"):
        shutil.copy(p, pout)
        continue

    pout = Path(pout.stripext()+"--converted"+pout.splitext()[-1])

    try:
        im = plt.imread(p)
    except:
        print(f"{p} cannot be read as an image.")
        continue

    h, w, layers = im.shape

    h2 = (w/ww)*hh
    w2 = (h/hh)*ww

    if h2 >= h:
        print(f"Increase height {h}->{h2}")
        left_right_bars = np.zeros([int(round(h2-h)/2), w, layers], dtype=im.dtype)

        imout = np.zeros([h+(left_right_bars.shape[0]*2), w, layers], dtype=im.dtype)
        for l in range(layers):
            imout[:,:,l] =(
                np.vstack((left_right_bars[:,:,l],
                           im[:,:,l],
                           left_right_bars[:,:,l])).astype(im.dtype)
                )

    else:
        print(f"Increase width {w}->{w2}")
        top_bottom_bars = np.zeros([h, int(round(w2-w)/2), layers], dtype=im.dtype)

        imout = np.zeros([h, w+(top_bottom_bars.shape[1]*2), layers], dtype=im.dtype)
        for l in range(layers):
            imout[:,:,l] =(
                np.hstack((top_bottom_bars[:,:,l],
                           im[:,:,l],
                           top_bottom_bars[:,:,l])).astype(im.dtype)
                )

    plt.imsave(pout, imout)