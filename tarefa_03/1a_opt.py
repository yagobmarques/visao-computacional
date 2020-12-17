import cv2  
import numpy as np
import sys
import math

def converterGrausParaRad(numero):
    rad = (numero/180)*math.pi
    return rad

def local_cantos(dst):
    cantos = []
    lim = 0.01*dst.max()
    for i in range(dst.shape[0]):
        for j in range(dst.shape[1]):
            if dst[i][j]>lim:
                cantos += [[i, j]]
    return cantos

def concatenate_string(strings):
    result = ""
    for i in range(len(strings)):
        result += strings[i]
        if i != len(strings)-1:
            result += "_"
    return result

def desenha_quadrado (i, img_vot):
    pxl_x = int(str.split(i[0], "_")[0] )
    pxl_y = int(str.split(i[0], "_")[1] )
    angle = int(str.split(i[0], "_")[2] )
    lado = int(str.split(i[0], "_")[3] )
    angle_cantos = []
    posi_cantos = []
    for i in range(4):
        angle_cantos.append(angle + 90 * (i+1))
    for j in range(4):
        angulo = converterGrausParaRad(angle_cantos[j])
        x = int(round(math.sin(angulo) * lado))
        y = int(round(math.cos(angulo) * lado))
        new_x = x+pxl_x
        new_y = y+pxl_y
        posi_cantos.append([new_x,new_y])
        img_vot[new_x][new_y]=[0, 0, 255]

    #desenhando as linhas do retangulo
    for h in range(4):

        if h == 3:
            start_point = (posi_cantos[h][1], posi_cantos[h][0])
            end_point = (posi_cantos[0][1], posi_cantos[0][0])
        else:
            start_point = (posi_cantos[h][1], posi_cantos[h][0])
            end_point = (posi_cantos[h+1][1], posi_cantos[h+1][0]) 
        color = (0, 255, 0) 
        thickness = 1
        img_vot = cv2.line(img_vot,  start_point, end_point, color, thickness)
        #img_vot[start_point[0]][start_point[1]]= [255,0,0]
    return 0
    

def square_detection(cantos, matriz_vot, img, max_tam):
    img_vot = np.zeros((img.shape))
    votados = []
    for cont in range(len(cantos)):
        votados.append(set())
    for l in np.arange (0, max_tam, 1):
        for o in np.arange (0, 360, 1):
            angle = converterGrausParaRad(o)
            x = int(round(math.cos(angle) * l))
            y = int(round(math.sin(angle) * l))
            for posi in range(len(cantos)):
                i = cantos[posi]
                # i[0] = eixo X; i[1] = eixo Y
                if i[0]+x >= 0 and i[0]+x < img.shape[0] and (x != 0 or y != 0):
                        if i[1]+y >= 0 and i[1]+y < img.shape[1]:
                            #matriz_vot[i[0]+x][i[0]+y][l][o] += 1
                            # blue = img_vot[i[0]+x][i[1]+y][0]
                            # green = img_vot[i[0]+x][i[1]+y][1]
                            # red = img_vot[i[0]+x][i[1]+y][2]
                            angle = o
                            if o > 90 and o <= 180:
                                angle = 180 - o
                            if o > 180 and o <= 270:
                                angle = 270 - o
                            if o > 270 and o <= 360:
                                angle = 360 - o
                            str_x = str(i[0]+x)
                            str_y = str(i[1]+y)
                            str_angle = str(angle)
                            str_l = str(l)
                            cat_strings = concatenate_string([str_x, str_y, str_angle, str_l])
                            if str_x + str_y not in votados[posi]:
                                # img_vot[i[0]+x][i[1]+y] = [blue+5, green+5, red+5]
                                if matriz_vot.get(cat_strings) == None:
                                    matriz_vot[cat_strings] = 1
                                else:
                                    matriz_vot[cat_strings] += 1
                                votados[posi].add(str_x+str_y)  
    print("Hough votation ended!")
    for i in matriz_vot.items():
        if int(i[1])==3:
            pxl_x = int(str.split(i[0], "_")[0] )
            pxl_y = int(str.split(i[0], "_")[1] )
            img_vot[pxl_x][pxl_y]=[0, 0, 255]
            #print("Quadrado de angulo: ", str.split(i[0], "_")[2] )
            desenha_quadrado(i, img_vot)
    cv2.imwrite("image.png", img_vot.astype(np.uint8))
    cv2. imshow("image.png", img_vot.astype(np.uint8))
    cv2.waitKey(0) 
    return 0
def main():
    try:
        pth_img = sys.argv[1]
        max_tam = int(sys.argv[2])
        img = cv2.imread(pth_img)
    except IndexError:
        max_tam = 100
    except:
        print("Opa, algum parâm")
        print("Para utilizar corretamente o programa utilize a sintaxe:")
        print("python 1a.py ./caminho_da_imagem tamanho_max_dos_quadrados(int)(default=100)")
        opt = input("Deseja saber mais sobre porque definir o tamanho máximo do quadrado? (yes/no)")
        if opt == "yes":
            print("É necessário colocar o tamanho dos quadrados para reduzir o runtime do algoritmo, caso não seja setado, será colocado um tamanho grande para que provavelmente atenda a todos os quadrados (demorado)")
        return -1
    img = cv2.imread(pth_img)
    ## Detecçao de cantos Harris
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.08)

    matriz_vot = dict()
    cantos = local_cantos(dst)
    square_detection(cantos, matriz_vot, img, max_tam)
    
if __name__ == '__main__':
    main()