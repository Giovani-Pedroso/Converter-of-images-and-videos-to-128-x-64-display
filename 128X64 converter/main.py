#Import the Libs for the GUI
from logging import disable
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import *
from kivy.uix.filechooser import FileChooserIconView 
from kivy.properties import ObjectProperty
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.uix.popup import Popup

#Import the OpenCv lib this lib is use to modify the images
import cv2 as cv

#Define the size of the program's window
Window.minimum_height = 400
Window.minimum_width = 1220

#Creation of an App object
class main_window(App):
    pass

#Creation of window App object
class Main_box(BoxLayout):
    
    
    input_image = ObjectProperty()
    output_image = ObjectProperty()

    input_file = ObjectProperty()
    output_file = ObjectProperty()

    #import_button = ObjectProperty()
    frame_slider = ObjectProperty()

    mode_spinner =ObjectProperty()
    inv_switch = ObjectProperty()

    parameter_1_slider = ObjectProperty()
    parameter_2_slider = ObjectProperty()

    resolution_spinner = ObjectProperty()
    
    image_out_x = 128
    image_out_y = 64

    inv = cv.THRESH_BINARY

    is_gif = False

    scren_output = (1600,800)
   

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
  
    def input(self,path):
        #self.input_image.source = org
        self.path = path[0]
        print(self.path)

        
        
        try:

            if self.path[-3:] == 'gif' or self.path[-3:] == 'mp4':
                
                self.is_gif = True
                print(2)
                self.gif = cv.VideoCapture(self.path)
                print(2)
                isTrue, self.image = self.gif.read()
                self.ids.frame_slider.disabled = False
                self.ids.frame_slider.max = int(self.gif.get(cv.CAP_PROP_FRAME_COUNT))
                self.update()
                
                pass

            else:
                print(1)
                self.is_gif = False
                print(1)
                self.image = cv.imread(self.path) 
                print(1)
                self.image_gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
                print(1)
                self.input_image.texture = self.set_texture(self.image)
                print(10)

            self.output_image.size_hint = (1, 1)
            self.input_file.size_hint =(None,None)
            self.input_file.size =(0,0)
            self.parameter_1_slider.disabled = False
            self.resolution_spinner.disabled = False

            self.ids.inverter_switch.disabled = False

            self.ids.bit_orientation_spinner.disabled = False
            self.ids.export_button.disabled = False
            self.ids.mode_spinner.disabled = False
            self.ids.export_button.disabled = False
            

            self.conversion()
            



        except Exception as e: 
            
            print("An exception occurred")
            print(e)
            popupWindow = Popup(title='Invalid file ,\nclick outside of window to exit', size_hint=(None,None), size=(240,100))
            popupWindow.open()
            #show_popup()
            #print(path[0])

    def call_input_screen(self):
        self.output_image.size_hint = (None, None)
        self.output_image.size = (0,0)
        self.input_file.size_hint =(1,1)


    #----------------------------------------------------------------------------------
    #
    #OpenCv Functions

    def set_texture(self,image):
        image = cv.flip(image,0)
        buf1 = image.tobytes()
        texture1 = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='bgr') 
        texture1.blit_buffer(buf1, colorfmt='bgr', bufferfmt='ubyte')
        
        return texture1

    def conversion(self):
        
        if self.ids.mode_spinner.text == 'Canny':

            self.parameter_2_slider.disabled = False
            self.ids.parameter_1_label.text = 'threshold value 1'
            self.ids.parameter_2_label.text = 'threshold value 2'
            self.parameter_1_slider.max = 1000
            self.parameter_2_slider.max = 1000
            self.canny()
            

        if self.ids.mode_spinner.text  == 'Adaptive threshold':

            
            self.ids.parameter_1_label.text = 'blockSize'
            self.ids.parameter_2_label.text = 'C'
            self.parameter_2_slider.disabled = False
            self.parameter_1_slider.max = 255
            self.parameter_2_slider.max = 255
            self.adap()

        if self.ids.mode_spinner.text  == 'Simple threshold':
            self.ids.parameter_1_label.text = 'threshold value'
            self.ids.parameter_2_label.text = ''
            self.parameter_2_slider.disabled = True
            self.parameter_1_slider.max = 255
            self.simple()

    def resolution_selection(self, widget):
        #'128x64','64x64','64x32','32x32','32x16','16x16','16x8','8x8'
        if widget.text == '128x64':
            self.image_out_x = 128
            self.image_out_y = 64
            self.scren_output= (1600,800)

        if widget.text == '64x64':
            self.image_out_x = 64
            self.image_out_y = 64
            self.scren_output= (1000,1000)


        if widget.text == '64x32':
            self.image_out_x = 64
            self.image_out_y = 32
            self.scren_output= (1600,800)

        if widget.text == '32x32':
            self.image_out_x = 32
            self.image_out_y = 32
            self.scren_output= (1000,1000)


        if widget.text == '32x16':
            self.image_out_x = 32
            self.image_out_y = 16
            self.scren_output= (1600,800)

        if widget.text == '16x16':
            self.image_out_x = 16
            self.image_out_y = 16
            self.scren_output= (1000,1000)


        if widget.text == '16x8':
            self.image_out_x = 16
            self.image_out_y = 8
            self.scren_output= (1600,800)

        if widget.text == '8x8':
            self.image_out_x = 8
            self.image_out_y = 8
            self.scren_output= (1000,1000)

        self.conversion()

    def simple(self):

        
        self.image_out = cv.resize(self.image_gray,(self.image_out_x,self.image_out_y))
        left , self.image_out =cv.threshold(self.image_out,int(self.parameter_1_slider.value)  , 255, self.inv )
        #
        copy_out =cv.cvtColor(cv.resize(self.image_out,(self.scren_output)),cv.COLOR_GRAY2RGB)
        
        self.output_image.texture =  self.set_texture(copy_out)

    def adap(self):

        
        self.image_out = cv.resize(self.image_gray,(self.image_out_x,self.image_out_y))
        val = int(self.parameter_1_slider.value)

        if not val % 2 or val==0:
            val += 1
            #main_window.parameter_0.setValue(val)


        self.image_out = cv.adaptiveThreshold(self.image_out, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,  self.inv ,val, int(self.parameter_2_slider.value))
        
        copy_out =cv.cvtColor(cv.resize(self.image_out,(self.scren_output )),cv.COLOR_GRAY2RGB)
        self.output_image.texture =  self.set_texture(copy_out)
 
    def canny(self):

        self.image_out = cv.resize(self.image_gray,(self.image_out_x,self.image_out_y))
        self.image_out = cv.Canny(self.image_out, int(self.parameter_1_slider.value), int(self.parameter_2_slider.value))
        
        copy_out =cv.cvtColor(cv.resize(self.image_out,(self.scren_output)),cv.COLOR_GRAY2RGB)
        
        self.output_image.texture =  self.set_texture(copy_out)


    def color_inv(self,widget):

        

        if not widget.active:
            self.inv = cv.THRESH_BINARY
        else:
            self.inv = cv.THRESH_BINARY_INV

        self.conversion()

    def update(self):
        

        self.gif.set(cv.CAP_PROP_POS_FRAMES, self.ids.frame_slider.value -1)
        isTrue, img = self.gif.read()
        self.input_image.texture =  self.set_texture(img)
    
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        temp_img = cv.resize(img,(self.scren_output), interpolation=cv.INTER_CUBIC)
        self.image_gray= cv.cvtColor(temp_img,cv.COLOR_RGB2GRAY)

        self.output_image.texture =  self.set_texture(temp_img)
        
        self.conversion()



    def img_2_bmp(self):
        
        
        #save_path = str(QFileDialog.getSaveFileName(filter='Text files (*.txt*)'))[2:-25]
        save_path = self.path[:-3] + 'txt'
        print(save_path)
        texto = open(save_path,'w')
        self.disable_all()
        try:
            if self.is_gif:
                total_frame = self.gif.get(cv.CAP_PROP_FRAME_COUNT)
                self.gif.set(cv.CAP_PROP_POS_FRAMES, 0)
                is_true, frame = self.gif.read()
                frame_gif = 0
                self.ids.frame_slider.value =0
                texto.write(f'const PROGMEM uint8_t gif[] = ' +'{//' f'resolution: x:{self.image_out_x} y:{self.image_out_y}, ' 'place &gif[/*frame number*/ * '+f'({self.image_out_x * self.image_out_x})]' + 'in the image plare of the draw function of your lib\n')

                while is_true:
                    
                    is_true, frame = self.gif.read()
                    print(frame_gif)
                    self.update()
                    texto.write(f'\n//---------------  frame {frame_gif} ---------------\n\n')
                    texto.write(self.bmp())
                    
                    frame_gif += 1
                    self.ids.frame_slider.value = frame_gif
        
        except:
            print(Exception)


        else:
                
            print('export image')
            texto.write(f'const PROGMEM uint8_t img[] = ' +'{\n')
            texto.write(self.bmp())
            

        texto.write('\n\n};')  
        texto.close()
        popupWindow = Popup(title='BMP ready\nsaved in the image\'s directory \nclick outside of window to exit', size_hint=(None,None), size=(240,100))
        popupWindow.open()
        self.enable_all()
            

    def bmp(self):
        img = self.image_out
        bmp =''
        eith_bits=0

        
        

        if self.ids.bit_orientation_spinner.text == 'vertical':
            height  = img.shape[1]
            width  = int(img.shape[0]/8)
            for z in range(width):
                
                for y in range(height):
                    
                #print(y)
                    for x in range(8):
                        if img[x+(8*z),y]!=0:
                            eith_bits |= (1<<x)
                                
                            
                    bmp += f' {hex(eith_bits)},' 
                    
                    eith_bits =0
                bmp += '\n'
            print('vertical')
            return bmp

        else:

            width = int(img.shape[1]/8)#largura
            height  = img.shape[0]#altura
            print(f'altura {height}')
            print(f'largura {width}')

            for z in range(height):
                
                for y in range(width):
                    
                #print(y)
                    for x in range(8):
                        if img[z, x+(8*y) ]!=0:
                            eith_bits |= (1<<(7-x))
                                
                            
                    bmp += f' {hex(eith_bits)},' 
                    
                    eith_bits =0

                bmp += '\n'
            print('horizontal')
            return bmp
  
    def disable_all(self):
        self.ids.import_button.disabled = True
        self.ids.frame_slider.disabled  = True

        self.parameter_1_slider.disabled = True
        self.parameter_2_slider.disabled = True
        self.resolution_spinner.disabled = True
        self.ids.inverter_switch.disabled = True
        self.ids.mode_spinner.disabled = True

        self.ids.bit_orientation_spinner.disabled = True
        self.ids.export_button.disabled = True
        
        

    def enable_all(self):
        self.ids.import_button.disabled = False
        self.ids.frame_slider.disabled  = False

        self.parameter_1_slider.disabled = False
        self.parameter_2_slider.disabled = False
        self.resolution_spinner.disabled = False
        self.ids.inverter_switch.disabled = False
        self.ids.mode_spinner.disabled = False

        self.ids.bit_orientation_spinner.disabled = False
        self.ids.export_button.disabled = False








        

#self.ids.'id do objeto'
main_window().run()


'''
    def save(self):
        self.input_image.size_hint =(None,None)
        self.input_image.size =(0,0)

        #self.output_file.size_hint = (1,1)
        #self.output_file.size=(0,0)
'''
        
