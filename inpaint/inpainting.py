import cv2
import numpy as np
import warnings
try:
    import numba
except:
    pass

warnings.filterwarnings("ignore", category=RuntimeWarning)

def inpaint(img,mask,**kwargs):

    '''
        Inpaints colored images using a moving median function.
        By using multiple windows the inpainting effect smooths
        through the masked area by moving toward the center and
        vice-versa for each subsequentlly added window with a
        max of 3.
        
        #####Input parameters#####
        img (image to be inpainted)
        mask (applied mask, using cv2.inRange or equivalent)
        kwargs include: window (window size, can be int or 1-3 int list)
                        numba (bool to optimize with numba **recommended**)

        #####Example calls#####
        inpaint(image,mask,window=3,numba=False)
        inpaint(image,mask,window=[3,5,8],numba=True)

        #####Defaults#####
        window = 3
        numba = False
    '''                                           

    window = [3]
    pass_no = 1
    numba = False

    for key, component in kwargs.items():
        if key == 'window':
            window = component
        elif key == 'numba':
            numba = component

    if type(window) == list:
        pass_no = len(window)
        if pass_no > 3:
            pass_no = 3
    else:
        window = [window]

    if numba:
        from filler2 import fill
    else:
        from filler1 import fill
        
    clone = img.copy()

    clone[:,:] = [0,0,0]
    clone[mask>0] = [255,255,255]

    imgray = cv2.cvtColor(clone, cv2.COLOR_BGR2GRAY)

    ret,thresh = cv2.threshold(imgray,50,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    mask_new = np.zeros(img.shape, np.uint8)
    mask_new = cv2.drawContours(mask_new, contours, -1, 255,1)

    find = np.unravel_index(np.where(mask_new.ravel()==255),mask_new.shape)

    run = True
    finder = []
    finder.append(find)
    indx = -1
    indx2 = 0

    while run:

        if len(find[0][0])!=0:

            try:
                img = fill(find,img,mask,window[0])
            except:
                pass

            mask[find[0],find[1]] = 0

            clone[mask>0] = [255,255,255]
            clone[mask==0] = [0,0,0]

            imgray = cv2.cvtColor(clone, cv2.COLOR_BGR2GRAY)

            ret,thresh = cv2.threshold(imgray,50,255,cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            
            mask_new = np.zeros(img.shape, np.uint8)

            mask_new = cv2.drawContours(mask_new, contours, -1, 255,1)
        
            find = np.unravel_index(np.where(mask_new.ravel()==255),mask_new.shape)
            finder.append(find)

            indx = len(finder)-1
            
        if len(find[0][0])==0:
            if pass_no==1:
                run = False
            else:

                if indx>=0:
                    try:
                        img = fill(finder[indx],img,mask,window[1])
                    except:
                        pass

                indx -= 1
                if indx<0:
                    if pass_no==2:
                        run = False
                    else:
                        try:
                            img = fill(finder[indx2],img,mask,window[2])
                        except:
                            pass

                        indx2 += 1
                        try:
                            if len(finder[indx2][0][0])==0:
                                run = False
                        except:
                            run = False
            
    return img

