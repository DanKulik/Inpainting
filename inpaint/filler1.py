import numpy as np
import warnings

warnings.simplefilter('once', UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

def fill(source,image,mask,rng):
    
    x = source[0][0]
    y = source[1][0]

    r = []
    g = []
    b = []

    for i in range(len(x)):


        xside = np.int(x[i])
        yside = np.int(y[i])
        
        x1 = np.int(xside-rng)
        x2 = np.int(xside+rng+1)  
        y1 = np.int(yside-rng)
        y2 = np.int(yside+rng+1)
    
        window = image[x1:x2,y1:y2]
        win_mask = mask[x1:x2,y1:y2]
        
        window = window[win_mask==0]
        window = np.transpose(window)
        colors = np.median(window, axis=1)
            
        r.append(colors[0])
        g.append(colors[1])
        b.append(colors[2])
    
    for i in range(len(x)):

        xside = np.int(x[i])
        yside = np.int(y[i])

        try:
            image[xside,yside]=[r[i],g[i],b[i]]  
        except:
            
            prob = """Contour region may extend to the images'
edge; or multiple contours may have
been detected. If image is distored, try
increasing the value of the single pass window radius.
Or if double pass the second window radius ect"""
            warnings.warn(prob)
            pass
        
    r.clear()
    g.clear()
    b.clear()
        
    return image
