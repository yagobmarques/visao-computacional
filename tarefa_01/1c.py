import cv2  
import numpy as np
import sys

def merge_images(img1 : np.ndarray, img2 : np.ndarray):
    if (img1.shape != img2.shape):
        print("Imagens incompatíveis")
        return -1
    img_final = np.zeros(img1.shape)
    img_final = np.add(0.5*img1, 0.5*img2)
    cv2.imshow("image", img_final.astype(np.uint8)) 
    cv2.waitKey(0) 
    return 0

def main():
    try:
        pth_img1 = sys.argv[1]
        pth_img2 = sys.argv[2]
        img1 = cv2.imread(pth_img1)
        img2 = cv2.imread(pth_img2)
        if img1.size == 0 or img2.size==0:
            raise Exception()
    except:
        print("Insira o caminho de uma imagem válida!")
        return -1
    merge_images(img1, img2)

if __name__ == '__main__':
    main()