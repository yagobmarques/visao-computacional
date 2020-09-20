import cv2  
import numpy as np
import sys

def split_channel(img : np.ndarray):
    img_B = img.copy()
    img_G = img.copy()
    img_R = img.copy()
    print(img_R.shape)
    # tirando os canais
    img_R[:,:,[0, 1]]= 0 
    img_B[:,:,[1, 2]]= 0
    img_G[:,:,[0, 2]]= 0
    img_final = np.concatenate((img_R, img_G, img_B), axis=1)
    cv2.imshow("image",img_final) 
    cv2.waitKey(0) 
    print("Os canais RGB foram separados!")
    return 1

def main():
    pth_img = ""
    ## Validando caminho da Imagem
    try:
        pth_img = sys.argv[1]
        img = cv2.imread(pth_img)
        if img.size == 0:
            raise Exception()
    except:
        print("Insira o caminho de uma imgem válida!")
        return -1
    split_channel(img)

if __name__ == '__main__':
    main()