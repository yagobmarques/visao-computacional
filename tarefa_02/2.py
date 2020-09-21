import cv2  
import numpy as np
import sys

def convolucao(amostra, kernel):
    conv = np.multiply(amostra, kernel)
    return abs(np.median(conv))

def median_filter(img : np.ndarray):
    kernel = np.ones((3,3), dtype="uint16")
    filtered_image = np.zeros(img.shape, dtype="uint16")
    for i in range(1, img.shape[0]-1):
        for j in range(1, img.shape[1]-1):
            filtered_image[i][j]= convolucao(img[i-1:i+2, j-1:j+2], kernel)
    return filtered_image

def main():
    try:
        pth_img = sys.argv[1]
        pth_saida = sys.argv[2]        
        img = cv2.imread(pth_img, 0)
    except:
        print("Argumentos inválidos")
        return -1
    img =median_filter(img)
    cv2.imwrite(pth_saida, img)
    
if __name__ == '__main__':
    main()