'''
Created on 13-feb.-2014

@author: Pepino
'''

from Tkinter import * 
from ScrolledText import ScrolledText
import Commands
import Queue
import matplotlib.pyplot as pp
from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import random, sin, exp
from PIL import Image,ImageTk
import threading, Queue
import GUIConnection
import time
import string
import math


class Plotter(Frame) : 
    
    
    
    def __init__(self,parent,max_x,max_y) : 
        Frame.__init__(self,parent)
        self.update_idletasks()
       
        self.x = 0
        self.y = 0
        self.y_2=0
        
        self.i = 0
        self.left_lim = 0
        self.update = 10  # to speed things up, never plot more than n_points on screen
        self.max_line=150
        self.max_x = max_x  
        self.interval=max_x  
        self.min_x = 0      
        self.xy_data = []
        self.xy_2_data =[]
        
        
        self.figure = pyplot.figure()
        # figsize (w,h tuple in inches) dpi (dots per inch)
        self.figure.set_size_inches((3,3), dpi=100, forward=True)
        self.subplot = self.figure.add_subplot(111)
        self.line, = self.subplot.plot([],[])
        
        #TODO:
        self.line_2, = self.subplot.plot([],[])
        
        
        pyplot.xlim(self.min_x,self.max_x)
        pyplot.ylim(0,max_y)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.stop = True
        self.canvas.get_tk_widget().grid()
        
        

    def plotter(self):
        self.x += 1
        
        self.xy_data += [[self.x,self.y]]
        
        
        self.xy_2_data += [[self.x,self.y_2]]
            
        self.min_x = self.x-self.interval
        self.max_x = self.x
        self.left_lim=self.i -self.interval
            
            
        if self.i<self.interval:
            self.left_lim =0
            self.min_x = 0
            self.max_x = self.interval
  
            
        if self.i>self.max_line:
            self.xy_2_data= self.xy_2_data[self.i-self.interval:self.i]
            self.xy_data= self.xy_data[self.i-self.interval:self.i]
            self.left_lim=0
            self.i = self.interval
        
        
            
        self.subplot.lines.remove(self.line) 
        self.subplot.lines.remove(self.line_2)
        pyplot.xlim(self.min_x,self.max_x)
        self.line, = self.subplot.plot(
                        [row[0] for row in self.xy_data[self.left_lim:self.i]],
                            [row[1] for row in self.xy_data[self.left_lim:self.i]],
                            color="blue")
        self.line_2, = self.subplot.plot(
                        [row[0] for row in self.xy_2_data[self.left_lim:self.i]],
                            [row[1] for row in self.xy_2_data[self.left_lim:self.i]],
                            color="red")
        
        
        self.i += 1
        self.canvas.draw()
        self.canvas.get_tk_widget().update_idletasks()
       
        #if self.stop == False:
        self.after(1500, self.plotter)
            



class GUI(Frame):
    
    zep_map_X_SCALE=5
    zep_map_Y_SCALE=4
    canvas_map_X_SCALE=5
    canvas_map_Y_SCALE=4
    fig_map_SCALE = 3
    
    
    
    
    def __init__(self,zeppelin):
        
        self.zep_state = {'height' : 0,'left-motor' : 0, 'right-motor':0, 'vert-motor':0, 'Goal':'not given', 'Error':'not given', 'Status':'not given' }
        self.zeppelin_database = zeppelinDatabase()
        
        self.zep_modus = 0
        
        
        self.parent = Tk()  
        Frame.__init__(self, self.parent, background="gray55") 
        
        self.zeppelin=zeppelin
        
        self.parent.title("Silver Surfer") 
        self.pack(fill=BOTH, expand=1) 
        
        self.btn_start = Button(self, text="START GUI" , command= self.start_protocol, background = "red",foreground = "white")
        self.btn_start.grid( sticky='WE') 
        
        self.img_silsur = Image.open('250px-Toss.png')
        imgr = self.img_silsur.resize((400, 400),Image.ANTIALIAS)
        self.img_silsur = ImageTk.PhotoImage(imgr)
        self.lbl_image_silsur = Label(self, image=self.img_silsur) 
        self.lbl_image_silsur.grid(row = 1, column = 0, padx = 5, pady = 5) 
        
        self.parser = GuiParser()
        self.compiler = GuiCompiler()
        
        self.parent.mainloop()
        
    
    def initGUI(self): 
        
        self.parent.geometry("1400x750") 
        #flags initialiseren
        self.flag_btn = False
        self.stop_show_height = True
        self.stop_show_motors = True
        #binden van buttons
        self.parent.bind('<Up>',self.move_forward)
        self.parent.bind('<Down>',self.move_backward)
        self.parent.bind('<Left>',self.turn_left)
        self.parent.bind('<Right>',self.turn_right)
        self.parent.bind('<a>',self.ascend)
        self.parent.bind('<d>',self.descend)
        
        self.parent.bind('<KeyRelease-Up>',self.h_release)
        self.parent.bind('<KeyRelease-Down>',self.h_release)
        self.parent.bind('<KeyRelease-Left>',self.h_release)
        self.parent.bind('<KeyRelease-Right>',self.h_release)
        self.parent.bind('<KeyRelease-a>',self.v_release)
        self.parent.bind('<KeyRelease-d>',self.v_release)
        
        
        
        #input
        self.Frame_input = Frame(self,background="gray55",padx=30)
        self.Frame_input.grid(row = 0, column = 0, sticky='WE') 
        
        
        btn_connection =  Button(self.Frame_input, text="MAKE CONNECTION" , command= self.connect_silver_surfer, background = "red",foreground = "white")
        btn_connection.grid(row = 1, column = 0, sticky = 'N') 
        
        self.view_state = 'test'  

        btn_connection =  Button(self.Frame_input, text="CHANGE VIEW" , command= self.invoke_change_view, background = "red",foreground = "white")
        btn_connection.grid(row = 2, column = 0, sticky = 'N') 
        
        
        self.Frame_picture= Frame(self.Frame_input)
        self.Frame_picture.grid(row = 0, column = 0)
        
        lbl_image = Label(self.Frame_picture, image=self.img_silsur) 
        lbl_image.grid(row = 0, column = 0) 
        
        
        self.Frame_control= Frame(self.Frame_input,background="gray55")
       
#Grote Stop knop
       
       
        btn_stop = Button(self.Frame_control, text="STOP" , command= self.stop, background = "red",foreground = "white")
        btn_stop.config( height = 5, width = 10) 
        btn_stop.grid(row = 0, column = 0, padx = 5, pady = 3, sticky='W') 
        
# #Grote Switch knop
#         
#         btn_switch = Button(self.Frame_control, text="SWITCH" , command= self.switch, background = "red",foreground = "white")
#         btn_switch.config( height = 5, width = 10) 
#         btn_switch.grid(row = 0, column = 2, padx = 5, pady = 3, sticky='W') 
        
       
#pijltjes, A en D
       
        self.Frame_btn_control = Frame(self.Frame_control,background="gray55")
        self.Frame_btn_control.grid(row = 0, column = 1) 
        
        rc_btn_height = 32 
        rc_btn_width = 34 
        
        self.motors_input = Entry(self.Frame_btn_control) 
        self.motors_input.grid(row = 1, column = 0,columnspan=2, sticky="WE")
        
        self.img_left = Image.open('pijlUPM1.png')
        imgr_left = self.img_left.resize((35, 50),Image.ANTIALIAS)
        self.img_left1 = ImageTk.PhotoImage(imgr_left)
        self.btn_M1 = Button(self.Frame_btn_control, image=self.img_left1,command= self.invoke_set_motors,background ="gray11",foreground = "white") #pijltje omhoog afbeelding #TODO:
        self.btn_M1.config( height = rc_btn_height, width = rc_btn_width ) 
        self.btn_M1.grid(row = 1, column = 4)

#         self.img_down = Image.open('pijlUPM2.png')
#         imgr_down = self.img_down.resize((35, 50),Image.ANTIALIAS)
#         self.img_down1 = ImageTk.PhotoImage(imgr_down)
#         self.btn_M2 = Button(self.Frame_btn_control, image=self.img_down1,background ="gray11",foreground = "white") #pijltje beneden afbeelding 
#         self.btn_M2.config( height = rc_btn_height, width = rc_btn_width ) 
#         self.btn_M2.grid(row = 2, column = 4) 
#         
#         self.img_up = Image.open('pijlDOWNM2.png')
#         imgr_up = self.img_up.resize((35, 50),Image.ANTIALIAS)
#         self.img_up1 = ImageTk.PhotoImage(imgr_up)
#         self.btn_up = Button(self.Frame_btn_control, image=self.img_up1,background ="gray11",foreground = "white") #pijltje omhoog afbeelding 
#         self.btn_up.config( height = rc_btn_height, width = rc_btn_width ) 
#         self.btn_up.grid(row = 2, column = 1 ,padx = 5, pady = 3)
        
#         
#         self.img_right = Image.open('pijlUPM3.png')
#         imgr_right = self.img_right.resize((35, 50),Image.ANTIALIAS)
#         self.img_right1 = ImageTk.PhotoImage(imgr_right)
#         self.btn_M3 = Button(self.Frame_btn_control, image=self.img_right1,background ="gray11",foreground = "white") #pijltje rechts afbeelding 
#         self.btn_M3.config( height = rc_btn_height, width = rc_btn_width ) 
#         self.btn_M3.grid(row = 3, column = 4 ) 
        
#         self.img_a = Image.open('pijlDOWNM1.png')
#         imgr_a = self.img_a.resize((35, 50),Image.ANTIALIAS)
#         self.img_a1 = ImageTk.PhotoImage(imgr_a)
#         self.btn_ascend = Button(self.Frame_btn_control, image=self.img_a1,background ="gray11",foreground = "white") #stijgen
#         self.btn_ascend.config( height = rc_btn_height, width = rc_btn_width ) 
#         self.btn_ascend.grid(row = 2, column = 0,padx = 5, pady = 3)
#         
#         self.img_d = Image.open('pijlDOWNM3.png')
#         imgr_d = self.img_d.resize((35, 50),Image.ANTIALIAS)
#         self.img_d1 = ImageTk.PhotoImage(imgr_d)
#         self.btn_descend = Button(self.Frame_btn_control, image=self.img_d1,background ="gray11",foreground = "white") #dalen
#         self.btn_descend.config( height = rc_btn_height, width = rc_btn_width ) 
#         self.btn_descend.grid(row = 2, column = 2 ,padx = 5, pady = 3)
        

        
        
        
        
        
        self.entry_input = Entry(self.Frame_control) 
        self.entry_input.config( width = 1 )
        self.entry_input.grid(row = 1, column = 0,columnspan=2, padx = 3, pady = 3,sticky="WE") 
        self.btn_input_enter = Button(self.Frame_control, text="STABILIZE",command= self.invoke_stabilize,background ="gray11",foreground = "white") 
        self.btn_input_enter.grid(row = 1, column = 3, padx = 2, pady = 3,sticky="WE")
        
        
        self.entry_input_move_to = Entry(self.Frame_control) 
        self.entry_input_move_to.config( width = 1 )
        self.entry_input_move_to.grid(row = 2, column = 0,columnspan=2, padx = 3, pady = 3,sticky="WE") 
        self.btn_input_enter_move_to = Button(self.Frame_control, text="MOVE TO",command= self.invoke_move_to,background ="gray11",foreground = "white") 
        self.btn_input_enter_move_to.grid(row = 2, column = 3, padx = 2, pady = 3,sticky="WE")
        
        self.Frame_control.grid(row = 3)
        
        
        
        
        
        
#         #binden GUI-stuurknoppen
#         
#         self.btn_up.bind("<Button-1>", self.move_forward)
#         self.btn_up.bind("<ButtonRelease-1>", self.h_release)
#         
#         self.btn_M2.bind("<Button-1>", self.move_backward)
#         self.btn_M2.bind("<ButtonRelease-1>", self.h_release)
#         
#         self.btn_M1.bind("<Button-1>", self.turn_left)
#         self.btn_M1.bind("<ButtonRelease-1>", self.h_release)
#         
#         self.btn_M3.bind("<Button-1>", self.turn_right)
#         self.btn_M3.bind("<ButtonRelease-1>", self.h_release)
#         
#         self.btn_ascend.bind("<Button-1>", self.ascend)
#         self.btn_ascend.bind("<ButtonRelease-1>", self.v_release)
#         
#         self.btn_descend.bind("<Button-1>", self.descend)
#         self.btn_descend.bind("<ButtonRelease-1>", self.v_release)
        
        
        self.Frame_AI = Frame(self,background="gray55")
        self.Frame_AI.grid(row=0,column=1)
        #Frame info andere zeppelins
        self.Frame_info_competition = Frame(self.Frame_AI,bg = "grey55",bd = 5,pady=10)
        self.positions_zeppelin_string_competition = StringVar()
        self.positions_zeppelin_string_competition.set(" \n \n \n \n   ---Info others---")
        self.lbl_title_frame_comp= Label(self.Frame_info_competition, bg = "grey55",fg="white", textvariable=self.positions_zeppelin_string_competition)
        self.lbl_title_frame_comp.grid(sticky='N')
        self.Frame_info_competition.grid(row=0)
        
        #Frame info silversurfer
        self.Frame_info_silversurfer = Frame(self.Frame_AI,bg = "grey55",borderwidth=5,pady=10)
        self.positions_zeppelin_string_silversurfer = StringVar()
        self.positions_zeppelin_string_silversurfer.set(" \n \n \n \n   ---Info silversurfer---")
        
        self.lbl_title_frame_zeps= Label(self.Frame_info_silversurfer, bg = "grey55",fg="white", textvariable=self.positions_zeppelin_string_silversurfer)
        self.lbl_title_frame_zeps.grid(sticky='S')
        self.Frame_info_silversurfer.grid(row = 1)
        
        
        
       
     
        
        
        
        
        self.Frame_output = Frame(self,background="gray55",padx=30)
        self.Frame_output.grid(row = 0, column = 2,  sticky='WE') 
        
        self.Frame_board = Frame(self.Frame_output,self,background="gray55",pady=30)
        self.Frame_board.grid(row = 0, columnspan =3)
        
        self.img_grid = Image.open('opvulses.png')
        imgr = self.img_grid.resize((400, 400),Image.ANTIALIAS)
        self.img_grid = ImageTk.PhotoImage(imgr)
        self.lbl_image_grid = Label(self.Frame_board, image=self.img_grid) 
        
        #MAP Zeppelins en rooster
        self.canvas_map_height = 400
        self.canvas_map_width = 500
        self.canvas_map = Canvas(self.Frame_output,height =self.canvas_map_height+20, width =self.canvas_map_width+20, bg = "white")
        self.canvas_map.grid(row = 0, column = 0, padx = 5, pady = 5,columnspan=3)
        
        #Dictionary met actieve canvas-zeppelinobjecte
        self.active_zeppelins = {} 
        
        
    
        self.Frame_visual_view=Frame(self.Frame_output,bg = "grey55")
        
        self.Frame_motors = Frame(self.Frame_output,background="gray55")
   
        
        self.img_motor_counter = Image.open('draai.png')
        imgr_motor_counter = self.img_motor_counter.resize((25, 25),Image.ANTIALIAS)
        self.img_motor_counter = ImageTk.PhotoImage(imgr_motor_counter)
        
        self.img_motor_clock = Image.open('draai2.png')
        imgr_motor_clock = self.img_motor_clock.resize((25, 25),Image.ANTIALIAS)
        self.img_motor_clock = ImageTk.PhotoImage(imgr_motor_clock)
        
        self.motor1 = StringVar()
        self.motor1.set('...')
        
        self.motor2 = StringVar()
        self.motor2.set('...')
        
        self.motor3 = StringVar()
        self.motor3.set('...')          
        
        self.goal = StringVar()
        self.goal.set('...')
        
        self.error = StringVar()
        self.error.set('...')
        
        self.height = StringVar()
        self.height.set('...')   
        
        motor_height_text_width = 10
        
        self.lbl_txt_motor1 = Label(self.Frame_motors,text="Motor 1 [L]", bg = "grey55",fg="white")
        self.lbl_txt_motor1.grid(row =1,column = 0 )
        self.lbl_motor1 = Label(self.Frame_motors, textvariable=self.motor1, width = motor_height_text_width, bg = "grey55",fg="white")
        self.lbl_motor1.grid(row = 1, column = 1, padx = 5, pady = 5,sticky='WE') 
        
        self.lbl_txt_motor1 = Label(self.Frame_motors,text="Motor 2 [R]", bg = "grey55",fg="white")
        self.lbl_txt_motor1.grid(row =2,column = 0 )
        self.lbl_motor2 = Label(self.Frame_motors, textvariable=self.motor2,width=motor_height_text_width, bg = "grey55",fg="white")
        self.lbl_motor2.grid(row = 2, column = 1, padx = 5, pady = 5,sticky='WE') 
        
        self.lbl_txt_motor1 = Label(self.Frame_motors,text="Motor 3 [Vert]", bg = "grey55",fg="white")
        self.lbl_txt_motor1.grid(row =3,column = 0 )
        self.lbl_motor3 = Label(self.Frame_motors, textvariable=self.motor3,width = motor_height_text_width, bg = "grey55",fg="white")
        self.lbl_motor3.grid(row = 3, column = 1, padx = 5, pady = 5,sticky='WE') 
        
        self.lbl_txt_motor1 = Label(self.Frame_motors,text="Goal", bg = "grey55",fg="white")
        self.lbl_txt_motor1.grid(row =4,column = 0 )
        self.lbl_goal = Label(self.Frame_motors, textvariable=self.goal,width = motor_height_text_width, bg = "grey55",fg="white")
        self.lbl_goal.grid(row = 4, column = 1, padx = 5, pady = 5,sticky='WE') 
        
        self.lbl_txt_motor1 = Label(self.Frame_motors,text="Height Error", bg = "grey55",fg="white")
        self.lbl_txt_motor1.grid(row =5,column = 0 )
        self.lbl_error = Label(self.Frame_motors, textvariable=self.error,width = motor_height_text_width, bg = "grey55",fg="white")
        self.lbl_error.grid(row = 5, column = 1, padx = 5, pady = 5,sticky='WE') 
        
               
        self.lbl_txt_motor1 = Label(self.Frame_motors,text="Height", bg = "grey55",fg="white")
        self.lbl_txt_motor1.grid(row =6,column = 0 )
        self.lbl_height = Label(self.Frame_motors, textvariable=self.height,width = motor_height_text_width, bg = "grey55",fg="white")
        self.lbl_height.grid(row = 6, column = 1, padx = 5, pady = 5,sticky='WE') 
        
        
        self.Frame_graphview = Frame(self.Frame_visual_view, bg = "grey55")
        self.Frame_graphview.config(width=200,height = 150)
        self.height_graph = Plotter(self.Frame_graphview,50,3)
        
        
        
        
        
        self.Frame_visual_view.grid(row = 1, column = 0, sticky='WE') 
        
        self.Frame_graphview.grid(row = 1,column=0)
        self.height_graph.grid()
        self.height_graph.plotter()
        self.Frame_motors.grid(row=1,column = 1)

        self.Frame_angle_vector = Frame(self.Frame_output, bg = "grey55")
        #vector map
        self.canvas_vector_height = 100
        self.canvas_vector_width = 100
        self.canvas_vector = Canvas(self.Frame_angle_vector,height =self.canvas_vector_height, width =self.canvas_vector_width, bg = "white")
        self.canvas_vector.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.Frame_angle_vector.grid(row=1,column=2)
        
        self.vector = Vector(self.canvas_vector,self.canvas_vector_width,self.canvas_vector_height)
        
        
        
        #AI view
        self.Frame_game_alfa = Frame(self.Frame_input)
        self.tb_AI_alfa = ScrolledText(self.Frame_game_alfa, undo=True)
        self.tb_AI_alfa['font'] = ('consolas', '12')
        self.tb_AI_alfa.config(width = 25, height = 10) 
        self.tb_AI_alfa.grid() 
 
        
        self.Frame_game_beta = Frame(self.Frame_input)
        self.tb_AI_beta = ScrolledText(self.Frame_game_beta, undo=True)
        self.tb_AI_beta['font'] = ('consolas', '12')
        self.tb_AI_beta.config(width = 40, height =20 )  
        self.tb_AI_beta.grid() 
        
        #recognized points
        self.recognized = {}
        

    def connect_silver_surfer(self):
        self.invoke_change_view()
        self.establish_connection()
        textfile = 'niks'
        self.load_map(self.canvas_map,textfile)
        self.height_graph.plotter()
        self.update_gui()
        
    
    def start_protocol(self,*args):
        self.parent.protocol("WM_DELETE_WINDOW", self.exit_protocol)  
        self.lbl_image_silsur.grid_remove()
        self.btn_start.grid_remove()
        self.initGUI()
        
    def invoke_change_view(self):
        if self.view_state is 'test':
            self.invoke_change_view_to_AI()
        else: 
            self.invoke_change_view_to_test()
            

            
 
        
    def invoke_change_view_to_AI(self):    
#         self.Frame_control.grid_remove()
        self.Frame_picture.grid_remove()
#         self.Frame_game_alfa.grid(row=3)
        self.Frame_game_beta.grid(row=0)

        self.view_state = 'AI'  
        
    def invoke_change_view_to_test(self):
#         self.Frame_game_alfa.grid_remove()
        self.Frame_game_beta.grid_remove()
#         self.Frame_control.grid(row=3)
        self.Frame_picture.grid(row=0,column=0)
        
        self.view_state = 'test'   
      
    
 
        
    
        
    
      
   
    def invoke_stabilize(self):
        height = self.entry_input.get()
        self.send_string_command('STABILIZE:' + str(int(height)))
       
        


   #test methodes 
    def pushed(self,*args):
        if self.flag_btn == False:
            print 'pushed'
            self.flag_btn=True
            
    def released(self,*args):
        if self.flag_btn == True:
            print 'released'
            self.flag_btn=False
         
    def pushed2(self,*args):
        if self.flag_btn == False:
            print 'pushed2'
            self.flag_btn=True
            
    def released2(self,*args):
        if self.flag_btn == True:
            print 'released2'
            self.flag_btn=False
            
    # einde testmethodes
    
    def h_release(self,*args):
        if self.flag_btn == True:
            self.h_stop()
            self.flag_btn=False
    
    def v_release(self,*args):
        if self.flag_btn == True:
            self.v_stop()
            self.flag_btn=False

    def move_forward(self,*args):
        if self.flag_btn == False:
            #command= Commands.Move(float('infinity'))
            #self.queue.put(command)
            self.send_string_command('V:' + 'infinity')
            self.flag_btn=True
          
            
    def turn_left(self,*args):
        if self.flag_btn == False:
            #command= Commands.Turn(float('-infinity'))
            #self.queue.put(command)
            self.send_string_command('L:' + 'infinity')
            self.flag_btn=True

    def turn_right(self,*args):
        if self.flag_btn == False:
            #command= Commands.Turn(float('infinity'))
            #self.queue.put(command)
            self.send_string_command('R:' +'infinity')
            self.flag_btn=True
        
    def move_backward(self,*args):
        if self.flag_btn == False:
            #command= Commands.Move(float('-infinity'))
            #self.queue.put(command)
            self.send_string_command('A:' + 'infinity')
            self.flag_btn=True
        
    def ascend(self,*args):
        if self.flag_btn == False:
            #command= Commands.Ascension(float('infinity')) #Commands.<Stijgen>
            #command= Commands.VertMove(100)
            #self.queue.put(command)
            self.send_string_command('S:' + 'infinity')
            self.flag_btn=True
        
    def descend(self,*args):
        if self.flag_btn == False:    
            #command= Commands.VertMove(-100)
            #self.queue.put(command)
            self.send_string_command('D:' + 'infinity')
            self.flag_btn=True
            

    
    def h_stop(self,*args):
        #command = Commands.HorStop()
        #self.queue.put(command)
        self.send_string_command('STOP:0')
        
    def v_stop(self,*args):
      #  command = Commands.VertStop()
        #command= Commands.VertMove(0)
        #self.queue.put(command)
        self.send_string_command('STOP:0')
    
        
    def stop(self,*args):
        #command = Commands.Stop()
        #self.queue.put(command)
        self.send_string_command('STOP:0')
        
    def switch(self,*args):
        new_modus = (self.zep_modus + 1) % 2
        self.send_string_command('SWITCH:' + str(new_modus))   
        
        
#EXTRA METHODES VOOR ZEPPELIN 2.0
    def invoke_set_motors(self,*args):
        ms= self.motors_input.get()
        ms_spl = ms.split(" ")
        self.GUIconnection.set_motors(ms_spl[0],ms_spl[1],ms_spl[2])
        
        
    def invoke_move_to(self,*args):
        coords= self.entry_input_move_to.get()
        coords_spl = coords.split(" ")
        self.GUIconnection.move_to(coords_spl[0],coords_spl[1],coords_spl[2])
        


    

        
#CONNECTIE
    def establish_connection(self):
        self.outputqueue  = Queue.Queue()
        self.inputqueue = Queue.Queue()
        self.GUIconnection = GUIConnection.GUIConn2dot1(self)
        self.GUIconnection.start()
        
        
    def load_map(self,cmap,textfile):
        map_compiler = GuiCompiler()
        #obj_coord is dictionaire
        #obj_coord[a]=[[x,y,color]]
        obj_coord = map_compiler.compile_map("field.csv", 40, self.canvas_map_width,self.canvas_map_height)
        
        for word in obj_coord:
            for coordinates_and_color in obj_coord[word]:
                map_compiler.objects[word](
                                           coordinates_and_color[0],
                                           coordinates_and_color[1],
                                           coordinates_and_color[2],
                                           cmap
                                           )
                
        
            
    def create_zeppelin(self,cmap,x,y):      
        return cmap.create_oval(GUI.zep_map_X_SCALE*(x-8),GUI.zep_map_Y_SCALE*y,GUI.zep_map_X_SCALE*x,GUI.zep_map_Y_SCALE*(y-8),fill='white')
    
    def create_dot(self,cmap,x,y):      
        return cmap.create_oval(GUI.zep_map_X_SCALE*(x-3),GUI.zep_map_Y_SCALE*y,GUI.zep_map_X_SCALE*x,GUI.zep_map_Y_SCALE*(y-3),fill='black')
        
    
    def move_zeppelin_to(self,zeppelin,cmap,x,y):
        cmap.coords(zeppelin,GUI.zep_map_X_SCALE*(x-8),GUI.zep_map_Y_SCALE*y,GUI.zep_map_X_SCALE*x,GUI.zep_map_Y_SCALE*(y-8)) 
        
    def move_dot_to(self,dot,cmap,x,y):
        cmap.coords(dot,GUI.zep_map_X_SCALE*(x-3),GUI.zep_map_Y_SCALE*y,GUI.zep_map_X_SCALE*x,GUI.zep_map_Y_SCALE*(y-3))     
        
    def move_text_to(self,text,cmap,x,y):  
        cmap.coords(text,GUI.zep_map_X_SCALE*x,GUI.zep_map_Y_SCALE*y) 
        
        
    def exit_protocol(self,*args):
        self.GUIconnection.connection_sender.close()
        self.GUIconnection.connection_consumer.close()
        self.after_idle(self.safe_exit)
        print 'Silver Surfer Terminated'
        
    def safe_exit(self,*args):
        self.parent.quit()
        self.parent.destroy()
        
    def send_string_command(self,string):
        self.GUIconnection.send_message_to_zep(string)
        

    
    def update_gui(self):
       
        try:
                string = self.inputqueue.get(False)
                self.take_care_of_message_string(string)   
                
        except Queue.Empty:
                #Do nothing
                pass
        
        
        
#         self.send_string_command("INFO:0")
# 
#         self.send_string_command("STATUS:0")

        self.update_graph_values()
        
        self.update_zeppelin_database()
        
        self.update_info_positions()
        
        self.update_map()
        
        self.update_motors()
        
        self.parent.after(1000, self.update_gui)
        
    def update_motors(self):
        self.motor1.set( str(int(self.zeppelin_database.zeppelins['silversurfer']['left-motor'])))
        self.motor3.set( str(int(self.zeppelin_database.zeppelins['silversurfer']['vert-motor'])))
        self.motor2.set(str(int(self.zeppelin_database.zeppelins['silversurfer']['right-motor'])))
        self.error.set( str(self.zeppelin_database.zeppelins['silversurfer']['Error']))
        self.goal.set( str(self.zeppelin_database.zeppelins['silversurfer']['Goal']))
        self.height.set(str(self.zeppelin_database.zeppelins['silversurfer']['z']))
        
        x=self.zeppelin_database.zeppelins['silversurfer']['left-motor']/100.0
        y=self.zeppelin_database.zeppelins['silversurfer']['right-motor']/100.0
        self.vector.setVector(x, y)
        
    def update_zeppelin_database(self):
        pass
        
    
    def update_graph_values(self):
        self.height_graph.y =  float(self.zeppelin_database.zeppelins['silversurfer']['z'])/100
        goal = self.zeppelin_database.zeppelins['silversurfer']['Goal']
        if goal == 'not given':
            self.height_graph.y_2 =0
        else:
            self.height_graph.y_2 = (float(goal)/100)
            
    def update_info_positions(self):
        info = '*----Position Zeppelins----* \n'
        for zep in self.zeppelin_database.zeppelins:
            info =(info + "------------ \n" + zep + "\n"+ 
                   'x: ' + str(self.zeppelin_database.zeppelins[zep]['x']) + '  '+ 
                   'y: ' + str(self.zeppelin_database.zeppelins[zep]['y']) + '  '+ 
                   'z: ' + str(self.zeppelin_database.zeppelins[zep]['z']) )                                                                                                  
        self.positions_zeppelin_string_competition.set(info)
        
        info =('*----Info SilverSurfer----* \n' + "------------ \n" + 
                   'goal_x: ' + str(self.zeppelin_database.zeppelins['silversurfer']['gx']) + '  '+ 
                   'goal_y: ' + str(self.zeppelin_database.zeppelins['silversurfer']['gy']) + '  '+ 
                   'goal_z: ' + str(self.zeppelin_database.zeppelins['silversurfer']['Goal'])) 
        self.positions_zeppelin_string_silversurfer.set(info) 
        
    def update_recognized(self,new_recognized):
        for point in new_recognized:
            if not(point in self.recognized):
                fig_point=self.create_dot(self.canvas_map,point[0],point[1])
                self.recognized[point] = fig_point

            else:
                self.move_dot_to(self.recognized[point], self.canvas_map,point[0],point[1]) 
       
         
        deleted_points=[]
        for point in self.recognized:
            if not(point in new_recognized):
                self.canvas_map.delete(self.recognized[point])
                deleted_points.append(point)
         
        for point in deleted_points:
            del self.recognized[point]   
    
            
    def update_map(self):
        #TODO: DEBUG!
        for zeppelin in self.zeppelin_database.zeppelins:
            if not(zeppelin in self.active_zeppelins):
                x=self.zeppelin_database.zeppelins[zeppelin]['x']
                y=self.zeppelin_database.zeppelins[zeppelin]['y']
                fig_zeppelin=self.create_zeppelin(self.canvas_map,x,y)
                self.active_zeppelins[zeppelin] = [fig_zeppelin,
                                                   self.canvas_map.create_text(x+5,y-2,text=zeppelin)]
            else:    
                x=self.zeppelin_database.zeppelins[zeppelin]['x']
                y=self.zeppelin_database.zeppelins[zeppelin]['y']
                self.move_zeppelin_to(self.active_zeppelins[zeppelin][0], self.canvas_map, x, y)
                self.move_text_to(self.active_zeppelins[zeppelin][1], self.canvas_map, x+5, y-2)
        for zeppelin in self.active_zeppelins:
            if not(zeppelin in self.zeppelin_database.zeppelins):
                self.canvas_map.delete(self.active_zeppelins[zeppelin][0])
                self.canvas_map.delete(self.active_zeppelins[zeppelin][1])
                
        
        
    def take_care_of_message_string(self,string):
        code = self.parser.parse_string_type(string)
        if code[0] == self.compiler.type_words[0]:
            self.update_SilverSurfer_dictionary(code[1])

        elif code[0] == self.compiler.type_words[1] and code[1] != "":
            if code[1] != self.zeppelin_database.zeppelins['silversurfer']['Status']: 
                self.print_in_textbox_decisions(string)
                self.zeppelin_database.zeppelins['silversurfer']['Status'] = code[1]
        
        elif code[0]== self.compiler.type_words[2] or code[0]== self.compiler.type_words[3]:
            self.print_in_textbox_decisions(string) 
        else:
            print "Reply: " + string
            
    def update_SilverSurfer_dictionary(self, state_string):

        parser = GuiParser()
        array_att = parser.parse_string_att(state_string)
        for s in array_att:
            att_and_val = s.split(':')
            self.zeppelin_database.zeppelins['silversurfer'][self.compiler.state_att_words[att_and_val[0]]]=float(att_and_val[1])
            
        
            
        
    def print_in_textbox_decisions(self,string):
        self.tb_AI_beta.insert(INSERT, str(string) + '\n')  
        self.tb_AI_beta.yview_pickplace("end")
        
    
        
class GuiParser():
    
    def parse_string_att(self,string):
        temp = string.split(';')
        return temp
    
    def parse_string_type(self, string):
        string = string.replace(' ','')
        temp = string.split('>')
        return temp
    
class Vector():
    def __init__(self,canvas,width,height):
        self.vector_canvas = canvas
        self.width = width
        self.height = height
        self.anchor=(width/2,height/2)
        self.b = width/10
        
        
        self.figure = self.vector_canvas.create_line(self.anchor[0],self.anchor[1],
                              self.anchor[0], 0,
                              width = self.b,
                              fill="red",
                              arrow=LAST)
        
    def setVector(self,x,y):
        top = (self.anchor[0]+x*self.anchor[0],self.anchor[1]-y*self.anchor[1])
        self.vector_canvas.coords(self.figure,self.anchor[0],self.anchor[1],top[0],top[1])
        
        
        

class GuiCompiler():
    
    def __init__(self):
        self.type_words = ["INFO", "STATUS","QR", "SWITCH", "SHUTDOWN"]
        self.state_att_words = { "H":"z", "GH":"Goal","E":"Error","LM":"left-motor","RM":"right-motor","VM":"vert-motor","Y":"y","X":"x","GY":"gy","GX":"gx","recognized":"recognized"}
        self.shapes = {'H' :"heart",'C':"circle",'S':"star",'R':"rectangle"}
        self.colors = {'W':"grey",'B':"blue",'G':"green",'R':"red",'Y':"yellow"}
        self.objects = {'rectangle':self.create_rectangle,'circle':self.create_circle,'star':self.create_star,'heart':self.create_hart}
        
    def create_rectangle(self,x_co,y_co,color,canvas):
        anchor_x = GUI.canvas_map_X_SCALE*x_co
        anchor_y = GUI.canvas_map_Y_SCALE*y_co
        canvas.create_rectangle(anchor_x,anchor_y,anchor_x+GUI.fig_map_SCALE*5,anchor_y+GUI.fig_map_SCALE *5,fill=color)
        
    def create_circle(self,x_co,y_co,color,canvas):
        anchor_x = GUI.canvas_map_X_SCALE*x_co
        anchor_y = GUI.canvas_map_Y_SCALE*y_co
        canvas.create_oval(anchor_x ,anchor_y,anchor_x+GUI.fig_map_SCALE*5,anchor_y+GUI.fig_map_SCALE*5,fill=color)
    
    def create_star(self,x_co,y_co,color,canvas):
        anchor_x = GUI.canvas_map_X_SCALE*x_co
        anchor_y = GUI.canvas_map_Y_SCALE*y_co
        canvas.create_polygon(anchor_x,anchor_y,
                              anchor_x+GUI.fig_map_SCALE*1, anchor_y+GUI.fig_map_SCALE*3,
                              anchor_x+GUI.fig_map_SCALE*3, anchor_y+GUI.fig_map_SCALE*3,
                              anchor_x+GUI.fig_map_SCALE*1, anchor_y+GUI.fig_map_SCALE*4,
                              anchor_x+GUI.fig_map_SCALE*3, anchor_y+GUI.fig_map_SCALE*8,
                              anchor_x, anchor_y+GUI.fig_map_SCALE*5,
                              anchor_x-GUI.fig_map_SCALE*3, anchor_y+GUI.fig_map_SCALE*8,
                              anchor_x-GUI.fig_map_SCALE*1, anchor_y+GUI.fig_map_SCALE*4,
                              anchor_x-GUI.fig_map_SCALE*3, anchor_y+GUI.fig_map_SCALE*3,
                              anchor_x-GUI.fig_map_SCALE*1, anchor_y+GUI.fig_map_SCALE*3,
                              anchor_x,anchor_y,
                              fill=color)
        
    def create_hart(self,x_co,y_co,color,canvas):
        anchor_x = GUI.canvas_map_X_SCALE*x_co
        anchor_y = GUI.canvas_map_Y_SCALE*y_co
        canvas.create_polygon(anchor_x,anchor_y,
                              anchor_x+GUI.fig_map_SCALE*1,anchor_y-GUI.fig_map_SCALE*1,
                              anchor_x+GUI.fig_map_SCALE*2,anchor_y-GUI.fig_map_SCALE*2,
                              anchor_x+GUI.fig_map_SCALE*3,anchor_y-GUI.fig_map_SCALE*1,
                              anchor_x+GUI.fig_map_SCALE*3,anchor_y+GUI.fig_map_SCALE*1,
                              anchor_x, anchor_y+GUI.fig_map_SCALE*5,
                              anchor_x-GUI.fig_map_SCALE*3,anchor_y+GUI.fig_map_SCALE*1,
                              anchor_x-GUI.fig_map_SCALE*3,anchor_y-GUI.fig_map_SCALE*1,
                              anchor_x-GUI.fig_map_SCALE*2,anchor_y-GUI.fig_map_SCALE*2,
                              anchor_x-GUI.fig_map_SCALE*1,anchor_y-GUI.fig_map_SCALE*1,
                              fill = color)    
      
    
        
    
    def test_map(self):
        return {'star':[[50,50,'blue'],[80,80,'red'],[80,40,'white'],[50,40,'black']],'rectangle':[[20,10,'grey']],'oval':[[6,6,'grey55']],'heart':[[60,90,'blue']]}    
        
        
    def compile_map(self,textfile,length_edge,canvas_x_length, canvas_y_length):
        
        
        f = open(textfile, 'r')
        count = 0
        file_dict={}
        for line in f:
            
            no_spaces = string.replace(line, " ", "")
  
            splitted_line = no_spaces.split(',')

            file_dict[count]=[]
            for figure in splitted_line:
                if (figure[0] != 'X' and figure[1] != 'X' ):
                    color = self.colors[figure[0]]
                    shape = self.shapes[figure[1]]
                    file_dict[count].append((color,shape))
                else:
                    file_dict[count].append(("Nothing","Nothing"))
               
                  
            count = count + 1
        
        
        f.close()
        
        self.length_x = (length_edge/2) +  (len(file_dict[0])-1)*length_edge
        self.length_height = math.sqrt(length_edge**2 - (length_edge/2)**2)
        self.length_y = self.length_height*(len(file_dict)-1)
        print len(file_dict)
        
        GUI.zep_map_X_SCALE = float(canvas_x_length)/float(self.length_x)
        GUI.zep_map_Y_SCALE = float(canvas_y_length)/float(self.length_y)
        GUI.canvas_map_X_SCALE =  GUI.zep_map_X_SCALE
        GUI.canvas_map_Y_SCALE =  GUI.zep_map_Y_SCALE
        

        
        #create datastructure map
        result = {}
        for shape in self.objects:
            result[shape]=[]
        for i in range(0,len(file_dict)):
            for j in range(0,len(file_dict[i])):
                if (file_dict[i][j][1] != "Nothing"):
                    extra = 0
                    if(i%2!=0):
                        extra = length_edge/2
      #TODO: Hier misschien werken met globaal anker (alles 10p naar onder en naar rechts: ANKER DAN OVERAL GEBRUIKEN!)             
                    result[file_dict[i][j][1]].append([extra+j*length_edge,i*self.length_height,file_dict[i][j][0]])
        
        return result


class zeppelinDatabase():
    
    def __init__(self):
        self.zeppelins = {'silversurfer':{'left-motor' : 0, 'right-motor':0, 'vert-motor':0, 'Goal':'not given', 'Error':'not given', 'Status':'not given','x':10,'y':10,'z':10,'gx':10,'gy':10 , 'recognized':[] }}

    def addZeppelin(self,name):
        self.zeppelins[name]={'x':0,'y':0,'z':0}
        
    
 
    
    
    

gui = GUI(0)

