import numpy as np
from numba import njit

@njit(cache=True, nogil=True)
def fill(source,image,mask,rng):

    x = source[0][0]
    y = source[1][0]

    r = []
    g = []
    b = []

    for i in range(len(x)):

        rr = []
        gg = []
        bb = []

        xside = np.int(x[i])
        yside = np.int(y[i])
        
        x1 = np.int(xside-rng)
        x2 = np.int(xside+rng+1)  
        y1 = np.int(yside-rng)
        y2 = np.int(yside+rng+1)
    
        window = image[x1:x2,y1:y2]
        win_mask = mask[x1:x2,y1:y2]

        for j in range(len(win_mask)):
            for k in range(len(win_mask)):
                if win_mask[j,k]==0:
                    rr.append(window[j,k,0])
                    gg.append(window[j,k,1])
                    bb.append(window[j,k,2])
                
        r.append(np.median(np.array(rr)))
        g.append(np.median(np.array(gg)))
        b.append(np.median(np.array(bb)))
        
        '''window = window[win_mask==0]
        window = np.transpose(window)
        colors = np.median(window, axis=1)
            
        r.append(colors[0])
        g.append(colors[1])
        b.append(colors[2])'''

        '''window = window[win_mask==0]
        r.append(np.median(window[:,:,0]))
        g.append(np.median(window[:,:,1]))
        b.append(np.median(window[:,:,2]))'''
    
    for i in range(len(x)):

        xside = np.int(x[i])
        yside = np.int(y[i])

        if not np.isnan(r[i]):
            image[xside,yside]=[r[i],g[i],b[i]]  
        
    r.clear()
    g.clear()
    b.clear()
        
    return image
