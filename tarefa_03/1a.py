import cv2  
import numpy as np
import sys
import math

def converterGrausParaRad(numero):
    rad = (numero/180)*math.pi
    return rad

def square_detection(dst, matriz_vot, img):
    lim = 0.01*dst.max()
    img_vot = np.zeros((img.shape))
    for i in range (dst.shape[0]):
        for j in range (dst.shape[1]):
            if (dst[i][j]>lim):
                # é um canto    
                votados = [[]]
                for l in np.arange (30, 60, 1):
                    for o in np.arange (0, 360, 1):
                        angle = converterGrausParaRad(o)
                        x = int(round(math.cos(angle) * l))
                        y = int(round(math.sin(angle) * l))
                        if i+x >= 0 and i+x < img.shape[0] and (x != 0 or y != 0):
                            if j+y >= 0 and j+y < img.shape[1]:
                                matriz_vot[i+x][j+y][l][o] += 1
                                blue = img_vot[i+x][j+y][0]
                                green = img_vot[i+x][j+y][1]
                                red = img_vot[i+x][j+y][2]
                                if [i+x, j+y] not in votados:
                                    img_vot[i+x][j+y] = [blue+5, green+5, red+5]
                                    votados += [[i+x, j+y]]       
    print("Hough votation ended!")
    
    cv2.imwrite("image.png", img_vot.astype(np.uint8))
    cv2. imshow("image.png", img_vot.astype(np.uint8))
    cv2.waitKey(0) 
    return 0
def main():
    
    try:
        pth_img = sys.argv[1]
        max_tam = sys.argv[2]
        
        img = cv2.imread(pth_img)
    except:
        print("Argumentos inválidos")
        print("Para utilizar corretamente o programa utilize a sintaxe:")
        print("python 1a.py ./caminho_da_imagem tamanho_max_dos_quadrados(int)")
        return -1
    
    ## Detecçao de cantos Harris
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.08)

    matriz_vot = np.zeros((img.shape[0], img.shape[1], 60, 90), dtype = np.int8)
    square_detection(dst, matriz_vot, img)
    
if __name__ == '__main__':
    main()