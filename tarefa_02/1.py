import cv2  
import numpy as np
import sys

def gamma_correction(img : np.ndarray, lvl_brilho):
    gamma = lvl_brilho
    invgamma = 1.0/gamma
    table = dict()
    for i in range(0, 256):
        table[i] =  (i/255) ** invgamma
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] = table[img[i][j]] * 255
    # cv2.imshow("image", img.astype(np.uint8)) 
    # cv2.waitKey(0) 
    return img

def black_strip(img : np.ndarray, largura_entre_faixas, largura_faixas):
    pxl_atual = 0
    width = img.shape[1]
    while pxl_atual+largura_faixas < width:
        img[:,pxl_atual: pxl_atual+largura_faixas]=0
        pxl_atual += largura_faixas + largura_entre_faixas
        if pxl_atual+largura_faixas >= width:
            img[:,pxl_atual:]=0
            break
    # cv2.imshow("image", img.astype(np.uint8)) 
    # cv2.waitKey(0) 
    return img

def main():
    try:
        pth_img = sys.argv[1]
        lvl_brilho = float(sys.argv[2])
        largura_entre_faixas = int(sys.argv[3])
        largura_faixas = int(sys.argv[4])
        pth_saida = sys.argv[5]        
        img = cv2.imread(pth_img, 0)
    except:
        print("Argumentos inválidos")
        return -1
    img = gamma_correction(img, lvl_brilho)
    img = black_strip (img, largura_entre_faixas, largura_faixas)
    cv2.imwrite(pth_saida, img)
    
if __name__ == '__main__':
    main()