import cv2  
import numpy as np
import sys

def convolucao(amostra, kernel, num):
  sum = 0
  for i in range(amostra.shape[0]):
    for j in range(amostra.shape[1]):
      sum += amostra[i][j] * kernel[i][j]
  return abs(sum)/num

def prewitte(img : np.ndarray):
    kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype = "float" )
    kernel_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype = "float" )
    gradient = np.zeros(img.shape, dtype="float")
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            grad_x = convolucao(img[i-1:i+2, j-1:j+2], kernel_x, 1)
            grad_y = convolucao(img[i-1:i+2, j-1:j+2], kernel_y, 1)
            gradient[i][j] = (grad_x ** 2 + grad_y ** 2) ** 0.5
    return gradient

def median_filter(img : np.ndarray, ordem : int):
    limiar = 60
    gradient = prewitte(img)
    if ordem % 2 == 0:
        ordem += 1
    margem = int((ordem + 1)/2)
    kernel = np.ones((ordem, ordem), dtype="uint16")
    filtered_image = np.zeros(img.shape, dtype="uint16")
    for i in range(margem, img.shape[0]-margem):
        for j in range(margem, img.shape[1]-margem):
            if gradient[i][j]<limiar:
                filtered_image[i][j]= convolucao(img[i-margem+1:i+margem, j-margem+1:j+margem], kernel, ordem*ordem)
            else:
                filtered_image[i][j]= img[i][j]
    return filtered_image

def main():
    
    try:
        pth_img = sys.argv[1]
        forca_suav = int(sys.argv[2])
        limiar = int(sys.argv[3])        
        img = cv2.imread(pth_img, 0)
    except:
        print("Argumentos inválidos")
        print("Para utilizar corretamente o programa utilize a sintaxe:")
        print("python 3.py caminho_da_imagem forca_da_suavisacao(int) limiar_prewitte(int)")
        return -1

    img = median_filter(img, forca_suav)
    cv2.imshow("image", img.astype(np.uint8))
    cv2.waitKey(0) 

if __name__ == '__main__':
    main()