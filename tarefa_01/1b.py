import cv2  
import numpy as np
import sys

def flip(img : np.ndarray):
    cv2.imshow("image",np.flip(img, axis=0)) 
    cv2.waitKey(0) 

def main():
    pth_img = ""
    ## Validando caminho da Imagem
    try:
        pth_img = sys.argv[1]
        img = cv2.imread(pth_img)
        if img.size == 0:
            raise Exception()
    except:
        print("Insira o caminho de uma imagem válida!")
        return -1
    flip(img)

if __name__ == '__main__':
    main()