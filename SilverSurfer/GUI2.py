'''
Created on 13-feb.-2014

@author: Pepino
'''

from Tkinter import * 
from ScrolledText import ScrolledText
import Commands
import Queue
#import matplotlib.pyplot as pp
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
        inch_w = 3
        inch_h = 2.3
        self.figure.set_size_inches((inch_w,inch_h), dpi=150, forward=True)
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
    ANCHOR_ROOT = 10
    WINDOW_WIDTH =1300
    WINDOW_HEIGHT = 800
    
    
    
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
        imgr = self.img_silsur.resize((GUI.WINDOW_WIDTH/4,GUI.WINDOW_HEIGHT/3),Image.ANTIALIAS)
        self.img_silsur = ImageTk.PhotoImage(imgr)
        self.lbl_image_silsur = Label(self, image=self.img_silsur) 
        self.lbl_image_silsur.grid(row = 1, column = 0, padx = 5, pady = 5) 
        
        self.parser = GuiParser()
        self.compiler = GuiCompiler()
        
        self.parent.mainloop()
        
    
    def initGUI(self): 
        self.parent.geometry(str(GUI.WINDOW_WIDTH)+"x"+str(GUI.WINDOW_HEIGHT)) 
        #flags initialiseren
        self.flag_btn = False
        self.stop_show_height = True
        self.stop_show_motors = True
        
        
        
        #input
        self.Frame_input = Frame(self,background="gray55")
        self.Frame_input.grid(row = 0, column = 0, sticky='WE') 
        
        
        btn_connection =  Button(self.Frame_input, text="MAKE CONNECTION" , command= self.connect_silver_surfer, background = "red",foreground = "white")
        btn_connection.grid(row = 1, column = 0, sticky = 'N') 
        
        self.view_state = 'zilver'  

        btn_connection =  Button(self.Frame_input, text="CHANGE" , command= self.invoke_change_view, background = "red",foreground = "white")
        btn_connection.grid(row = 2, column = 0, sticky = 'N') 
        
        
        self.Frame_picture= Frame(self.Frame_input)
        self.Frame_picture.grid(row = 0, column = 0)
        
        lbl_image = Label(self.Frame_picture, image=self.img_silsur) 
        lbl_image.grid(row = 0, column = 0) 
        
        
        self.Frame_control= Frame(self.Frame_input,background="gray55")
       
#pijltjes, A en D
       
        self.Frame_btn_control = Frame(self.Frame_control,background="gray55")
        self.Frame_btn_control.grid(row = 0, column = 1) 
        
        rc_btn_height = GUI.WINDOW_HEIGHT/20
        rc_btn_width = GUI.WINDOW_WIDTH/40
        
        self.motors_input = Entry(self.Frame_control) 
        self.motors_input.grid(row = 0, column = 0,columnspan=2, sticky="WE")
        
        
        self.btn_M1 = Button(self.Frame_control, text="MOTORS",command= self.invoke_set_motors,background ="gray11",foreground = "white") #pijltje omhoog afbeelding #TODO:
        self.btn_M1.grid(row = 0, column = 3)  
        
        
        
        
        self.entry_input = Entry(self.Frame_control) 
        self.entry_input.config( width = 1 )
        self.entry_input.grid(row = 1, column = 0,columnspan=2, padx = 3, pady = 3,sticky="WE") 
        self.btn_input_enter = Button(self.Frame_control, text="PARAMETERS",command= self.invoke_parameters,background ="gray11",foreground = "white") 
        self.btn_input_enter.grid(row = 1, column = 3, padx = 2, pady = 3,sticky="WE")
        
        
        self.entry_input_move_to = Entry(self.Frame_control) 
        self.entry_input_move_to.config( width = 1 )
        self.entry_input_move_to.grid(row = 2, column = 0,columnspan=2, padx = 3, pady = 3,sticky="WE") 
        self.btn_input_enter_move_to = Button(self.Frame_control, text="MOVE TO",command= self.invoke_move_to,background ="gray11",foreground = "white") 
        self.btn_input_enter_move_to.grid(row = 2, column = 3, padx = 2, pady = 3,sticky="WE")
        
        self.Frame_control.grid(row = 3)
        
        self.Frame_output = Frame(self,background="gray55")
        self.Frame_output.grid(row = 0, column = 2,  sticky='WE') 
        
        self.Frame_AI = Frame(self,background="gray55")
        self.Frame_AI.grid(row=0,column=1)
        #Frame info andere zeppelins
        self.Frame_info_competition = Frame(self.Frame_output,bg = "grey55",bd = 5,pady=10)
        self.positions_zeppelin_string_competition = StringVar()
        self.positions_zeppelin_string_competition.set(" \n \n \n \n   ---Info positions---")
        self.lbl_title_frame_comp= Label(self.Frame_info_competition, bg = "grey55",fg="white", textvariable=self.positions_zeppelin_string_competition)
        self.lbl_title_frame_comp.grid(sticky='N')
        self.Frame_info_competition.grid(row=1,column=0)
        
        #Frame info silversurfer
        self.Frame_motors = Frame(self.Frame_input,background="gray55")
        
        self.Frame_info_silversurfer = Frame(self.Frame_motors,bg = "grey55",borderwidth=5,pady=10)
        self.positions_zeppelin_string_silversurfer = StringVar()
        self.positions_zeppelin_string_silversurfer.set("-----")

        self.lbl_title_frame_zeps= Label(self.Frame_info_silversurfer, bg = "grey55",fg="white", textvariable=self.positions_zeppelin_string_silversurfer)
        self.lbl_title_frame_zeps.grid(sticky='S')
        self.Frame_info_silversurfer.grid(row = 6,columnspan = 2)
        
        
        

        
        self.Frame_board = Frame(self.Frame_output,self,background="gray55")
        self.Frame_board.grid(row = 0, columnspan =3)
        
        self.img_grid = Image.open('opvulses.png')
        imgr = self.img_grid.resize((GUI.WINDOW_HEIGHT/4, GUI.WINDOW_WIDTH/4),Image.ANTIALIAS)
        self.img_grid = ImageTk.PhotoImage(imgr)
        self.lbl_image_grid = Label(self.Frame_board, image=self.img_grid) 
        
        #MAP Zeppelins en rooster
        self.canvas_map_height = GUI.WINDOW_HEIGHT/3
        self.canvas_map_width = GUI.WINDOW_WIDTH*6/16
        self.canvas_map = Canvas(self.Frame_output,height =self.canvas_map_height+20, width =self.canvas_map_width+20, bg = "white")
        self.canvas_map.grid(row = 0, column = 0, padx = 5, pady = 5,columnspan=3)
        
        #Dictionary met actieve canvas-zeppelinobjecte
        self.active_zeppelins = {} 
        
        
    
        self.Frame_visual_view=Frame(self.Frame_output,bg = "grey55")
        
 
   
        
        
        self.motor1 = StringVar()
        self.motor1.set('...')
        
        self.motor2 = StringVar()
        self.motor2.set('...')
        
        self.motor3 = StringVar()
        self.motor3.set('...')          
        
        self.goal = StringVar()
        self.goal.set('...')
        
        self.state = StringVar()
        self.state.set('...')
        
        self.height = StringVar()
        self.height.set('...')   
        
        motor_height_text_width = 10
        
        self.lbl_txt_motor1 = Label(self.Frame_motors,text="Motor 1 [L]", bg = "grey55",fg="white")
        self.lbl_txt_motor1.grid(row =1,column = 0 )
        self.lbl_motor1 = Label(self.Frame_motors, textvariable=self.motor1, width = motor_height_text_width, bg = "grey55",fg="white")
        self.lbl_motor1.grid(row = 1, column = 1, padx = 5, pady = 1,sticky='WE') 
        
        self.lbl_txt_motor1 = Label(self.Frame_motors,text="Motor 2 [R]", bg = "grey55",fg="white")
        self.lbl_txt_motor1.grid(row =2,column = 0 )
        self.lbl_motor2 = Label(self.Frame_motors, textvariable=self.motor2,width=motor_height_text_width, bg = "grey55",fg="white")
        self.lbl_motor2.grid(row = 2, column = 1, padx = 5, pady = 1,sticky='WE') 
        
        self.lbl_txt_motor1 = Label(self.Frame_motors,text="Motor 3 [Vert]", bg = "grey55",fg="white")
        self.lbl_txt_motor1.grid(row =3,column = 0 )
        self.lbl_motor3 = Label(self.Frame_motors, textvariable=self.motor3,width = motor_height_text_width, bg = "grey55",fg="white")
        self.lbl_motor3.grid(row = 3, column = 1, padx = 5, pady = 1,sticky='WE') 
        
        self.lbl_txt_motor1 = Label(self.Frame_motors,text="Goal", bg = "grey55",fg="white")
        self.lbl_txt_motor1.grid(row =4,column = 0 )
        self.lbl_goal = Label(self.Frame_motors, textvariable=self.goal,width = motor_height_text_width, bg = "grey55",fg="white")
        self.lbl_goal.grid(row = 4, column = 1, padx = 5, pady = 1,sticky='WE') 
        
        self.lbl_txt_motor1 = Label(self.Frame_motors,text="State", bg = "grey55",fg="white")
        self.lbl_txt_motor1.grid(row =5,column = 0 )
        self.lbl_error = Label(self.Frame_motors, textvariable=self.state,width = motor_height_text_width, bg = "grey55",fg="white")
        self.lbl_error.grid(row = 5, column = 1, padx = 5, pady = 1,sticky='WE') 
        
               
        self.lbl_txt_motor1 = Label(self.Frame_motors,text="Height", bg = "grey55",fg="white")
        self.lbl_height = Label(self.Frame_motors, textvariable=self.height,width = motor_height_text_width, bg = "grey55",fg="white")

        
        
        self.Frame_graphview = Frame(self.Frame_visual_view, bg = "grey55")
        self.Frame_graphview.config(width=200,height = 150)
        self.height_graph = Plotter(self.Frame_graphview,50,3)
        
        
        
        
        
        self.Frame_visual_view.grid(row = 1, column = 1, sticky='WE') 
        
        self.Frame_graphview.grid(row = 1,column=0)
        self.height_graph.grid()
        self.height_graph.plotter()
        self.Frame_motors.grid(row=4,column = 0)

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
        self.tb_AI_beta.config(width = 20, height =12)  
        self.tb_AI_beta.grid() 
        
        self.Frame_picture.grid_remove()
#         self.Frame_game_alfa.grid(row=3)
        self.Frame_game_beta.grid(row=0)
        
        #recognized points
        self.recognized = {}
        

    def connect_silver_surfer(self):
        self.establish_connection()
        textfile = 'field.csv'
        self.load_map(self.canvas_map,textfile)
        self.height_graph.plotter()
        self.update_gui()
        
    
    def start_protocol(self,*args):
        self.parent.protocol("WM_DELETE_WINDOW", self.exit_protocol)  
        self.lbl_image_silsur.grid_remove()
        self.btn_start.grid_remove()
        self.initGUI()
        
    def invoke_change_view(self):
        if self.view_state is 'zilver':
            self.view_state = 'zilver_simulator' 
        else: 
            self.view_state = 'zilver'  
      
       
        
#EXTRA METHODES VOOR ZEPPELIN 2.0
    def invoke_set_motors(self,*args):
        ms= self.motors_input.get()
        ms_spl = ms.split(" ")
        self.GUIconnection.set_motors(ms_spl[0],ms_spl[1],ms_spl[2],self.view_state)
        
        
    def invoke_move_to(self,*args):
        coords= self.entry_input_move_to.get()
        coords_spl = coords.split(" ")
        self.GUIconnection.move_to(coords_spl[0]+"0",coords_spl[1]+"0",coords_spl[2]+"0",self.view_state)
        
    def invoke_parameters(self):
        param = self.entry_input.get()
        self.GUIconnection.set_parameters(param,self.view_state)

    

        
#CONNECTIE
    def establish_connection(self):
        self.outputqueue  = Queue.Queue()
        self.inputqueue = Queue.Queue()
        self.GUIconnection = GUIConnection.GUIConn2dot1(self)
        self.GUIconnection.start()
        
        
    def load_map(self,cmap,textfile):
        map_compiler = GuiCompiler()
        compiled = map_compiler.compile_map(textfile, 40, self.canvas_map_width,self.canvas_map_height)
        obj_coord = compiled[0]
        lines= compiled[1]
        tablets = compiled[2]
        
        i_max = len(lines)
        for i in range(i_max):
            j_max = len(lines[i])
            for j in range(j_max):
                    if (j!=j_max-1):
                        if(lines[i][j][0]!="Nothing" and lines[i][j+1][0]!="Nothing"):
                            self.create_line(cmap,lines[i][j][0],lines[i][j][1], lines[i][j+1][0],lines[i][j+1][1])
                    if(i<i_max-1):
                        if(i%2!=0 and lines[i][j][0]!="Nothing" ):
                            if(lines[i+1][j][0]!="Nothing"):
                                self.create_line(cmap,lines[i][j][0],lines[i][j][1], lines[i+1][j][0],lines[i+1][j][1])
                            if(j<j_max-1 and lines[i+1][j+1][0]!="Nothing"):
                                    self.create_line(cmap,lines[i][j][0],lines[i][j][1], lines[i+1][j+1][0],lines[i+1][j+1][1])
                        if(i%2==0 and lines[i][j][0]!="Nothing" ):
                            if( lines[i+1][j][0]!="Nothing"):
                                self.create_line(cmap,lines[i][j][0],lines[i][j][1], lines[i+1][j][0],lines[i+1][j][1])
                            if(j>0 and lines[i+1][j-1][0]!="Nothing"):
                                self.create_line(cmap,lines[i][j][0],lines[i][j][1], lines[i+1][j-1][0],lines[i+1][j-1][1])
        for word in obj_coord:
            for coordinates_and_color in obj_coord[word]:
                map_compiler.objects[word](
                                           coordinates_and_color[0],
                                           coordinates_and_color[1],
                                           coordinates_and_color[2],
                                           cmap
                                           )
        for tab in tablets:
            map_compiler.create_rectangle(tab[0]/10, tab[1]/10, "Black", cmap)
        
            
    def create_zeppelin(self,cmap,x,y):
        anchor_x = GUI.canvas_map_X_SCALE*x-GUI.fig_map_SCALE*2+GUI.ANCHOR_ROOT
        anchor_y = GUI.canvas_map_Y_SCALE*y-GUI.fig_map_SCALE*2+GUI.ANCHOR_ROOT
        return cmap.create_oval(anchor_x ,anchor_y,anchor_x+GUI.fig_map_SCALE*5,anchor_y+GUI.fig_map_SCALE*5,fill="white")      
    
    
    
    def create_dot(self,cmap,x,y):      
        return cmap.create_oval(GUI.zep_map_X_SCALE*(x-3)+GUI.ANCHOR_ROOT,
                                GUI.zep_map_Y_SCALE*y+GUI.ANCHOR_ROOT,
                                GUI.zep_map_X_SCALE*x+GUI.ANCHOR_ROOT,
                                GUI.zep_map_Y_SCALE*(y-3)+GUI.ANCHOR_ROOT,fill='black')
    
    def create_line(self,cmap,x1,y1,x2,y2): 
        cmap.create_line(GUI.zep_map_X_SCALE*x1+GUI.ANCHOR_ROOT
                         ,GUI.zep_map_Y_SCALE*y1+GUI.ANCHOR_ROOT,
                         GUI.zep_map_X_SCALE*x2+GUI.ANCHOR_ROOT,
                         GUI.zep_map_Y_SCALE*y2+GUI.ANCHOR_ROOT) 
        
    
    def move_zeppelin_to(self,zeppelin,cmap,x,y):
        anchor_x = GUI.canvas_map_X_SCALE*x-GUI.fig_map_SCALE*2+GUI.ANCHOR_ROOT
        anchor_y = GUI.canvas_map_Y_SCALE*y-GUI.fig_map_SCALE*2+GUI.ANCHOR_ROOT
        cmap.coords(zeppelin,anchor_x ,anchor_y,anchor_x+GUI.fig_map_SCALE*5,anchor_y+GUI.fig_map_SCALE*5) 
        
    def move_dot_to(self,dot,cmap,x,y):
        cmap.coords(dot,GUI.zep_map_X_SCALE*(x-3)+GUI.ANCHOR_ROOT,
                    GUI.zep_map_Y_SCALE*y+GUI.ANCHOR_ROOT,
                    GUI.zep_map_X_SCALE*x+GUI.ANCHOR_ROOT
                    ,GUI.zep_map_Y_SCALE*(y-3)+GUI.ANCHOR_ROOT)     
        
    def move_text_to(self,text,cmap,x,y):  
        cmap.coords(text,GUI.zep_map_X_SCALE*x+GUI.ANCHOR_ROOT,GUI.zep_map_Y_SCALE*y+GUI.ANCHOR_ROOT) 
        
        
    def exit_protocol(self,*args):
        self.GUIconnection.connection_sender.close()
        self.GUIconnection.connection_consumer.close()
        self.after_idle(self.safe_exit)
        print 'Silver Surfer Terminated'
        
    def safe_exit(self,*args):
        self.parent.quit()
        self.parent.destroy()
        
    def send_string_command(self,string):
        self.GUIconnection.send_message_to_zep(string,self.view_state)
        

    
    def update_gui(self):
       

        self.update_graph_values()
        
        self.update_zeppelin_database()
        
        self.update_info_positions()
        
        self.update_map()
        
        self.update_motors()
        
        self.parent.after(1000, self.update_gui)
        
    def update_motors(self):
        self.motor1.set( str(int(self.zeppelin_database.zeppelins[self.view_state]['left-motor'])))
        self.motor3.set( str(int(self.zeppelin_database.zeppelins[self.view_state]['vert-motor'])))
        self.motor2.set(str(int(self.zeppelin_database.zeppelins[self.view_state]['right-motor'])))
        self.state.set(self.view_state)
        self.goal.set( str(self.zeppelin_database.zeppelins[self.view_state]['Goal']))
        self.height.set(str(self.zeppelin_database.zeppelins[self.view_state]['z']))
        
        x=self.zeppelin_database.zeppelins[self.view_state]['left-motor']/100.0
        y=self.zeppelin_database.zeppelins[self.view_state]['right-motor']/100.0
        self.vector.setVector(x, y)
        
    def update_zeppelin_database(self):
        pass
        
    
    def update_graph_values(self):
        self.height_graph.y =  float(self.zeppelin_database.zeppelins[self.view_state]['z'])/100
        goal = self.zeppelin_database.zeppelins[self.view_state]['Goal']
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
                   'z: ' + str(self.zeppelin_database.zeppelins[zep]['z']) +"\n")                                                                                                  
        self.positions_zeppelin_string_competition.set(info)
        
        info =(    'goal_x: ' + str(self.zeppelin_database.zeppelins[self.view_state]['gx']) + '  '+ 
                   'goal_y: ' + str(self.zeppelin_database.zeppelins[self.view_state]['gy']) + '  '+ 
                   'goal_z: ' + str(self.zeppelin_database.zeppelins[self.view_state]['Goal'])+ '\n'+
                   'Ci: ' + str(self.zeppelin_database.zeppelins[self.view_state]['Ci'])+'  '+ 
                   'Cd: ' + str(self.zeppelin_database.zeppelins[self.view_state]['Cd'])+'  '+ 
                   'Kp: ' + str(self.zeppelin_database.zeppelins[self.view_state]['Kp'])+'\n'+ 
                   'Kd: ' + str(self.zeppelin_database.zeppelins[self.view_state]['Kd'])+'  '+ 
                   'Ki: ' + str(self.zeppelin_database.zeppelins[self.view_state]['Ki'])+'  '+ 
                   'BIAS: ' + str(self.zeppelin_database.zeppelins[self.view_state]['BIAS'])+'\n'+ 
                   'MAX_PID_OUTPUT: '+ str(self.zeppelin_database.zeppelins[self.view_state]['MAX_PID_OUTPUT'])+'  '+ 
                   'MAX_Ci: '+ str(self.zeppelin_database.zeppelins[self.view_state]['MAX_Ci'])
                   ) 
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
            if self.zeppelin_database.zeppelins[zeppelin]['x'] != 'not given':
                if not(zeppelin in self.active_zeppelins):
                    x=self.zeppelin_database.zeppelins[zeppelin]['x']
                    y=self.zeppelin_database.zeppelins[zeppelin]['y']
                    fig_zeppelin=self.create_zeppelin(self.canvas_map,x,y)
                    self.active_zeppelins[zeppelin] = [fig_zeppelin,self.canvas_map.create_text(x+5,y-2,text=zeppelin)]
                else:    
                    x=self.zeppelin_database.zeppelins[zeppelin]['x']
                    y=self.zeppelin_database.zeppelins[zeppelin]['y']
                    self.move_zeppelin_to(self.active_zeppelins[zeppelin][0], self.canvas_map, x, y)
                    self.move_text_to(self.active_zeppelins[zeppelin][1], self.canvas_map, x+5, y-2)
        for zeppelin in self.active_zeppelins:
            if not(zeppelin in self.zeppelin_database.zeppelins):
                self.canvas_map.delete(self.active_zeppelins[zeppelin][0])
                self.canvas_map.delete(self.active_zeppelins[zeppelin][1])
                
        
        
            
    def update_SilverSurfer_dictionary(self, state_string):

        parser = GuiParser()
        array_att = parser.parse_string_att(state_string)
        for s in array_att:
            att_and_val = s.split(':')
            self.zeppelin_database.zeppelins[self.view_state][self.compiler.state_att_words[att_and_val[0]]]=float(att_and_val[1])
            
        
            
        
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
        self.colors = {'W':"grey",'B':"blue",'G':"green",'R':"red",'Y':"yellow",'X':"nothing"}
        self.objects = {'rectangle':self.create_rectangle,'circle':self.create_circle,'star':self.create_star,'heart':self.create_hart}
        
    def create_rectangle(self,x_co,y_co,color,canvas):
        anchor_x = GUI.canvas_map_X_SCALE*x_co-GUI.fig_map_SCALE*2+GUI.ANCHOR_ROOT
        anchor_y = GUI.canvas_map_Y_SCALE*y_co-GUI.fig_map_SCALE*2+GUI.ANCHOR_ROOT
        canvas.create_rectangle(anchor_x,anchor_y,anchor_x+GUI.fig_map_SCALE*5,anchor_y+GUI.fig_map_SCALE *5,fill=color)
        
    def create_circle(self,x_co,y_co,color,canvas):
        anchor_x = GUI.canvas_map_X_SCALE*x_co-GUI.fig_map_SCALE*2+GUI.ANCHOR_ROOT
        anchor_y = GUI.canvas_map_Y_SCALE*y_co-GUI.fig_map_SCALE*2+GUI.ANCHOR_ROOT
        canvas.create_oval(anchor_x ,anchor_y,anchor_x+GUI.fig_map_SCALE*5,anchor_y+GUI.fig_map_SCALE*5,fill=color)
    
    def create_star(self,x_co,y_co,color,canvas):
        anchor_x = GUI.canvas_map_X_SCALE*x_co+GUI.ANCHOR_ROOT
        anchor_y = GUI.canvas_map_Y_SCALE*y_co-GUI.fig_map_SCALE*3+GUI.ANCHOR_ROOT
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
        anchor_x = GUI.canvas_map_X_SCALE*x_co+GUI.ANCHOR_ROOT
        anchor_y = GUI.canvas_map_Y_SCALE*y_co+GUI.ANCHOR_ROOT
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
        count = -1
        file_dict={}
        tablets=[]
        for line in f:
            
            no_spaces = string.replace(line, " ", "")
  
            splitted_line = no_spaces.split(',')

            
            
            if(no_spaces[0]in self.colors):
                count = count + 1
                file_dict[count]=[]
            else:
                tablets.append((int(splitted_line[0]),int(splitted_line[1])))
            
            for figure in splitted_line:
                if(figure[0] in self.colors and figure[1] in self.shapes):
                    color = self.colors[figure[0]]
                    shape = self.shapes[figure[1]]
                    file_dict[count].append((color,shape))
            


            
            
               
                  
            
        
        
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
        coords_pairs={}
        for shape in self.objects:
            result[shape]=[]
            
        for i in range(0,len(file_dict)):
            coords_pairs[i] = {}
            for j in range(0,len(file_dict[i])):
                coords_pairs[i][j]=("Nothing","Nothing")
                if (file_dict[i][j][1] != "Nothing"):
                    extra = 0
                    if(i%2!=0):
                        extra = length_edge/2
                        
      #TODO: Hier misschien werken met globaal anker (alles 10p naar onder en naar rechts: ANKER DAN OVERAL GEBRUIKEN!)             
                    result[file_dict[i][j][1]].append([extra+j*length_edge,i*self.length_height,file_dict[i][j][0]])
                    coords_pairs[i][j]=(extra+j*length_edge,i*self.length_height)
        return result,coords_pairs, tablets


class zeppelinDatabase():
    
    def __init__(self):
        self.zeppelins = {'zilver':{'left-motor' : 0, 
                                          'right-motor':0, 
                                          'vert-motor':0, 
                                          'Goal':'not given', 
                                          'Error':'not given', 
                                          'Status':'not given',
                                          'x':'not given',
                                          'y':'not given',
                                          'z':0,
                                          'gx':0,
                                          'gy':0, 
                                          'recognized':[],
                                          'Ci':'not given',
                                          'Cd':'not given' ,
                                          'Kp':'not given' ,
                                          'Kd':'not given' ,
                                          'Ki':'not given' ,
                                          'BIAS':'not given' ,
                                          'MAX_PID_OUTPUT':'not given' ,
                                          'MAX_Ci':'not given'},
                          'zilver_simulator':{'left-motor' : 0, 
                                          'right-motor':0, 
                                          'vert-motor':0, 
                                          'Goal':'not given', 
                                          'Error':'not given', 
                                          'Status':'not given',
                                          'x':'not given',
                                          'y':'not given',
                                          'z':0,
                                          'gx':0,
                                          'gy':0 , 
                                          'recognized':[],
                                          'Ci':'not given',
                                          'Cd':'not given' ,
                                          'Kp':'not given' ,
                                          'Kd':'not given' ,
                                          'Ki':'not given' ,
                                          'BIAS':'not given' ,
                                          'MAX_PID_OUTPUT':'not given' ,
                                          'MAX_Ci':'not given'}}
    def addZeppelin(self,name):
        self.zeppelins[name]={'x':0,'y':0,'z':0}
        
    
 
    
    
    

gui = GUI(0)

