import cv2  
import numpy as np
import sys

def gradient(width : int, heigth : int):
    adctio = 256/heigth
    actual = 0
    img_grad = np.zeros((heigth, width, 3))
    for i in range (heigth):
        for j in range (width):
            img_grad[i][j]= [actual, actual, actual]
        actual = actual + adctio
    cv2.imshow("image", img_grad.astype(np.uint8)) 
    cv2.waitKey(0) 
    return 0

def main():
    try:
        width = int(sys.argv[1])
        heigth = int(sys.argv[2])
        if width <= 0 or heigth <=0:
            raise Exception()
    except:
        print("Tamanhos válidos!")
        return -1
    gradient(width, heigth)

if __name__ == '__main__':
    main()