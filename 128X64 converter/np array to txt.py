import numpy as np
import cv2 as cv
img = cv.imread('/home/cleide/Área de Trabalho/ima bmp.png')
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
print(img.shape)

bmp =''
eith_bits=0
array = np.array([[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],#16x16
                  [1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1],
                  [1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,1],
                  [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
                  [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
                  [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1],
                  [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1],
                  [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
                  [0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
                  [0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
                  [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
                  [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
                  [0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
                  [0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1],
                  [0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
                  [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],], dtype='uint8')


def img_2_bmp_v(img):
    bmp =''
    eith_bits=0

    width  = int(img.shape[0]/8)
    print(width)

    height  = img.shape[1]
    print(height)

    for z in range(width):
        print(z)
        for y in range(height):
            #print(y)
            for x in range(8):
                if img[x+(8*z),y]!=0:
                    eith_bits |= (1<<x)
                    
                
            bmp += f' {hex(eith_bits)},' 
            eith_bits =0
        bmp += '\n'

    print(bmp)
        
    texto = open('ok.txt','w')
    texto.write(f'const PROGMEM uint8_t img[] = ' +'{\n')
    texto.write(bmp)
    texto.write('};')
    texto.close()
    
def img_2_bmp_h(img):
    bmp =''
    eith_bits=0

    width  = int(img.shape[0]/8)
    print(width)

    height  = img.shape[1]
    print(height)

    for z in range(width):
        print(z)
        for y in range(height):
            #print(y)
            for x in range(8):
                if img[x+(8*z),y]!=0:
                    eith_bits |= (1<<x)
                    
                
            bmp += f' {hex(eith_bits)},' 
            eith_bits =0
        bmp += '\n'

    print(bmp)
        
    texto = open('ok.txt','w')
    texto.write(f'const PROGMEM uint8_t img[] = ' +'{\n')
    texto.write(bmp)
    texto.write('};')
    texto.close()

img_2_bmp_v(img)










'''
bmp =''
eith_bits=0

width  = int(img.shape[0]/8)
print(width)

height  = img.shape[1]
print(height)

for z in range(width):
    print(z)
    for y in range(height):
        #print(y)
        for x in range(8):
            if img[x+(8*z),y]!=0:
                eith_bits |= (1<<x)
                
            
        bmp += f' {hex(eith_bits)},' 
        eith_bits =0
    bmp += '\n'
'''
