import cv2, numpy as np, sys, math
from matplotlib import pyplot as plt
import random

kwargs = dict(arg.split('=') for arg in sys.argv[2:])

#o tamanho padrao e 1024x768
img = np.zeros((768, 1024)).astype(np.uint8)
H, W = img.shape

#se vai utilizar um tamanho fixo
fixedSize = 'size' in kwargs
#se vai utilizar um angulo fixo
fixedTheta = 'angle' in kwargs
#se vai utilizar um numero de quadrados fixo
fixedNumber = 'number' in kwargs
#se vai testar sobreposicao
overlapTest = 'overlapTest' in kwargs

if fixedNumber:
	n = int(kwargs['number'])
else:
	n = random.randint(3, 100)

def side(p0, p1, q):
	v0 = (p1[0] - p0[0], p1[1] - p0[1])
	v1 = (q[0]  - p0[0], q[1]  - p0[1])
	return v0[0]*v1[1] - v0[1]*v1[0]

print(n)
rects = []
k = 0
while k < n:
	if fixedSize:
		size = int(kwargs['size'])
	else:
		size = random.randint(4, 30)
	#hd: metade da diagonal
	hd = math.sqrt(2)*size/2
	if fixedTheta:
		angle = float(kwargs['angle'])
	else:
		angle = random.random()*math.pi/2
	theta = angle + math.pi/4
	y = random.randint(int(size), H-1-int(size))
	x = random.randint(int(size), W-1-int(size))
	pts = []
	for i in range(4):
		pts.append((x+hd*math.cos(theta+i*math.pi/2), y-hd*math.sin(theta+i*math.pi/2)))
	s = (pts[0], pts[1], pts[2], pts[3])
	overlap = False
	if overlapTest:
		for r in rects:
			for i in range(4):
				for j in range(4):
					v0 = (s[i], s[(i+1)%4])
					v1 = (r[j], r[(j+1)%4])
					side0 = side(v0[0], v0[1], v1[0])*side(v0[0], v0[1], v1[1])
					side1 = side(v1[0], v1[1], v0[0])*side(v1[0], v1[1], v0[1])
					if side0 < 0 and side1 < 0:
						overlap = True
	if not overlap:
		k += 1
		print(str(x) + ' ' + str(y) + ' ' + str(size) + ' ' + str(angle))
		rects.append((pts[0], pts[1], pts[2], pts[3]))
		cv2.fillPoly(img, np.int32([pts]), 255)

cv2.imshow('janela', img.astype(np.uint8))
cv2.imwrite(sys.argv[1], img)
cv2.waitKey(0)