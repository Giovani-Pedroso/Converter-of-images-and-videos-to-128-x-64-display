from PyQt5 import QtGui, QtCore, QtWidgets,uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap, QImage
import cv2 as cv
import numpy as np

global gif, img_out, input_gray, is_gif
play = False
check = True
inv = cv.THRESH_BINARY 

app = QtWidgets.QApplication([])
main_window = uic.loadUi('128X64 converter/128x64 converter.ui')

def Import():
    global input_gray, gif, is_gif
  
    path_file = str(QFileDialog.getOpenFileName(filter='Image(*.*)'))[2:-16]
    archive_format = path_file[-3:]

    main_window.mode_box.show()
    main_window.label.show()
    main_window.parameter_0.show()
    main_window.checkBox.show()
    main_window.label_3.show()
    main_window.comboBox.show()
    main_window.export_code.show()
    main_window.export_image.show()


    if  archive_format == 'gif' or archive_format == 'mp4':

        is_gif = True

        main_window.frame_slider.show()

        gif = cv.VideoCapture(path_file)
        isTrue, img = gif.read()

        main_window.frame_slider.setMaximum(int(gif.get(cv.CAP_PROP_FRAME_COUNT)))

        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        temp_img = cv.resize(img,(600,300), interpolation=cv.INTER_CUBIC)
        input_gray = cv.cvtColor(temp_img,cv.COLOR_RGB2GRAY)

        main_window.img_input.setPixmap(Open2Pix(temp_img))

        conv()

    else:

        is_gif = False

        #hide the play buttom and the slider, because they are
        #useless im static images  
        main_window.frame_slider.hide()
        
        img = cv.imread(path_file)        
        
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        temp_img = cv.resize(img,(600,300), interpolation=cv.INTER_CUBIC)
        input_gray = cv.cvtColor(temp_img,cv.COLOR_RGB2GRAY)
        
        main_window.img_input.setPixmap(Open2Pix(temp_img))
        

        conv()


def Open2Pix(img):
    height, width, channel = img.shape
    bytesPerLine = 3 * width
    qImg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
    pixMap = QtGui.QPixmap.fromImage(qImg)
    return pixMap


def conv():
    
    if main_window.mode_box.currentText() == 'Canny':
        main_window.parameter_0.setMaximum(1000)
        main_window.parameter_1.setMaximum(1000)
        main_window.checkBox.hide()
        
        main_window.parameter_0.setSingleStep(20)
        main_window.parameter_1.setSingleStep(20)

        main_window.parameter_1.show()
        main_window.label_2.show()

        main_window.label.setText('threshold1')
        main_window.label_2.setText('threshold2')

        Canny()
        

    if main_window.mode_box.currentText() == 'Adaptive threshold':

        main_window.parameter_0.setMaximum(200)
        main_window.parameter_1.setMaximum(200)

        main_window.checkBox.show()
        main_window.parameter_1.show()
        main_window.label_2.show()

        main_window.label.setText('blockSize')
        main_window.label_2.setText('C')

        main_window.parameter_0.setSingleStep(6)
        main_window.parameter_1.setSingleStep(6)

        adap()

    if main_window.mode_box.currentText() == 'Simple threshold':

        main_window.label.setText('threshol value')

        main_window.parameter_0.setMaximum(255)
        main_window.parameter_0.setSingleStep(6)

        main_window.checkBox.show()
        
        main_window.parameter_1.hide()
        main_window.label_2.hide()
        
        simple()


def simple():

    global input_gray, img_out,inv
    img_out = cv.resize(input_gray,(128,64))
    left , img_out =cv.threshold(img_out, main_window.parameter_0.value() , 255, inv)
    
    copy_out =cv.cvtColor(cv.resize(img_out,(600,300)),cv.COLOR_GRAY2RGB)
    
    main_window.img_output.setPixmap(Open2Pix(copy_out))
    

def adap():

    global input_gray, img_out,inv
    img_out = cv.resize(input_gray,(128,64))
    val = main_window.parameter_0.value()

    if not val % 2:
        val += 1
        main_window.parameter_0.setValue(val)


    img_out = cv.adaptiveThreshold(img_out, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, inv ,val,main_window.parameter_1.value())
    
    copy_out =cv.cvtColor(cv.resize(img_out,(600,300)),cv.COLOR_GRAY2RGB)
    
    main_window.img_output.setPixmap(Open2Pix(copy_out))


def Canny():
    global input_gray, img_out
    img_out = cv.resize(input_gray,(128,64))
    img_out = cv.Canny(img_out, main_window.parameter_0.value(), main_window.parameter_1.value())
    
    copy_out =cv.cvtColor(cv.resize(img_out,(400,200)),cv.COLOR_GRAY2RGB)
    
    main_window.img_output.setPixmap(Open2Pix(copy_out))


def check_box():

    global check, inv
    check = not check

    if check:
        inv = cv.THRESH_BINARY
    else:
        inv = cv.THRESH_BINARY_INV

    conv()


def update():
    global gif,input_gray
    gif.set(cv.CAP_PROP_POS_FRAMES, main_window.frame_slider.value()-1)
    isTrue, img = gif.read()

    
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    temp_img = cv.resize(img,(600,300), interpolation=cv.INTER_CUBIC)
    input_gray = cv.cvtColor(temp_img,cv.COLOR_RGB2GRAY)

    main_window.img_input.setPixmap(Open2Pix(temp_img))

    conv()


def img_2_bmp():
    
    global gif, img_out
    total_frame = gif.get(cv.CAP_PROP_FRAME_COUNT)
    save_path = str(QFileDialog.getSaveFileName(filter='Text files (*.txt*)'))[2:-25]
    print(save_path)
    texto = open(save_path,'w')
    

    if is_gif:
        main_window.progressBar.show()
        gif.set(cv.CAP_PROP_POS_FRAMES, 0)
        is_true, frame = gif.read()
        frame_gif = 0
        texto.write(f'const PROGMEM uint8_t gif[] = ' +'{//place &gif[/*frame number*/ * 1024] in the image plare of the draw function of your lib\n')

        while is_true:
            
            is_true, frame = gif.read()
            print(frame_gif)
            update()
            texto.write(f'\n//---------------  frame {frame_gif} ---------------\n\n')
            texto.write(bmp())
            
            frame_gif += 1
            main_window.frame_slider.setValue(frame_gif)
            main_window.progressBar.setValue(int(100 * frame_gif/total_frame))

    else:
            
        
        texto.write(f'const PROGMEM uint8_t img[] = ' +'{\n')
        texto.write(bmp())
        

    main_window.progressBar.hide()
    texto.write('\n\n};')  
    texto.close()
        

def bmp():
    img = img_out
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
    return bmp


#hide the unnecessary stuff in the inicialization
main_window.label_2.hide()
main_window.progressBar.hide()
main_window.frame_slider.hide()
main_window.parameter_1.hide()

main_window.mode_box.hide()
main_window.label.hide()
main_window.parameter_0.hide()
main_window.checkBox.hide()
main_window.label_3.hide()
main_window.comboBox.hide()
main_window.export_code.hide()
main_window.export_image.hide()

#main_window.img_output.setAlignment(Qt.AlignCenter)



#link the functions to the screen elements
main_window.checkBox.toggled.connect(check_box)
main_window.parameter_0.valueChanged.connect(conv)
main_window.parameter_1.valueChanged.connect(conv)
main_window.export_code.clicked.connect(img_2_bmp)
main_window.mode_box.currentTextChanged.connect(conv)

main_window.frame_slider.valueChanged.connect(update)
main_window.Import.clicked.connect(Import)

main_window.show()
app.exec()