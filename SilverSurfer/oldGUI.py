'''
Created on 23-nov.-2013

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

class Plotter(Frame) : #te hard coded? herbruikbaar?
    def __init__(self,parent,max_x,max_y) : #extra method als handler (get height blablabla)
        Frame.__init__(self,parent)
        self.update_idletasks()
        self.x = 0
        self.i = 0
        self.left_lim = 0
        self.update = 10  # to speed things up, never plot more than n_points on screen
        self.max_line=150
        self.max_x = max_x  
        self.interval=max_x  
        self.min_x = 0      
        self.xy_data = []
        self.figure = pyplot.figure()
        # figsize (w,h tuple in inches) dpi (dots per inch)
        self.figure.set_size_inches((5,5), dpi=100, forward=True)
        self.subplot = self.figure.add_subplot(111)
        self.line, = self.subplot.plot([],[])
        pyplot.xlim(self.min_x,self.max_x)
        pyplot.ylim(0,max_y)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.stop = True
        self.canvas.get_tk_widget().grid()

    def plotter(self):
        self.x += 1
        self.y = abs(random.randn())
        self.xy_data += [[self.x,self.y]]
            
        self.min_x = self.x-self.interval
        self.max_x = self.x
        self.left_lim=self.i -self.interval
            
            
        if self.i<self.interval:
            self.left_lim =0
            self.min_x = 0
            self.max_x = self.interval
  
            
        if self.i>self.max_line:
            self.xy_data= self.xy_data[self.i-self.interval:self.i]
            self.left_lim=0
            self.i = self.interval
        
        
            
        self.subplot.lines.remove(self.line) 
        pyplot.xlim(self.min_x,self.max_x)
        self.line, = self.subplot.plot(
                        [row[0] for row in self.xy_data[self.left_lim:self.i]],
                            [row[1] for row in self.xy_data[self.left_lim:self.i]],
                            color="blue")
        self.i += 1
        self.canvas.draw()
        self.canvas.get_tk_widget().update_idletasks()
       
        if self.stop == False:
            self.after(10000, self.plotter)


class GUI(Frame):
    
     
    def __init__(self, queue,zeppelin): 
        self.parent = Tk() 
        self.parent.geometry("1300x650+300+300") 
        Frame.__init__(self, self.parent, background="gray55") 
        self.zeppelin=zeppelin
        self.initGUI() 
        self.queue=queue
        self.parent.mainloop()
        
        
    def initGUI(self): 
        self.parent.title("Blimp bizkit") #Titel moet door zeppling worden gestuurd 
        self.pack(fill=BOTH, expand=1) 
        
        #flag_btn init op false
        self.flag_btn = False
        self.stop_show_height = True
        
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
        self.Frame_input = Frame(self,background="gray55")
        self.Frame_input.grid(row = 0, column = 0, sticky='W') 
        
        self.img1 = Image.open('sample.png')
        imgr = self.img1.resize((400, 400),Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(imgr)
        self.lbl_image = Label(self.Frame_input, image=self.img) #TODO: image juist adress. 
        #lbl_image = Label(self.Frame_input, text="Afbeelding")
        #lbl_image.config(width = 70, height = 30) 
        self.lbl_image.grid(row = 0, column = 0, padx = 5, pady = 5, columnspan=3) 
        
        # 3 Menu knoppen 
        menu_btn_width = 7 
        menu_btn_height = 1
        
        self.Frame_cmenu = Frame(self.Frame_input,background="gray55")
        self.Frame_cmenu.config(width= 1)
        self.Frame_cmenu.grid(row = 1, column = 0,  sticky='W') 
        
        btn_record = Button(self.Frame_cmenu, text="RECORD",background ="gray11",foreground = "white") 
        btn_record.config( height = menu_btn_height, width = menu_btn_width ) 
        btn_record.grid(row = 1, column = 0, padx = 5, pady = 3, columnspan = 1,sticky='W') 
        
        btn_pic = Button(self.Frame_cmenu, text="TAKE PIC",background ="gray11",foreground = "white") 
        btn_pic.config( height = menu_btn_height, width = menu_btn_width ) 
        btn_pic.grid(row = 2, column = 0, padx = 5, pady = 3, columnspan = 1,sticky='W') #Manual input 
       
       
        btn_command = Button(self.Frame_cmenu, text="COMMAND" , command= self.invoke_command,background ="gray11",foreground = "white" )
        btn_command.config( height = menu_btn_height, width = menu_btn_width + 3 ) 
        btn_command.grid(row = 3, column = 0, padx = 5, pady = 3, sticky='W') 
          
            
            
        entry_input = Entry(self.Frame_input) 
        entry_input.config( width = 1 )
        entry_input.grid(row = 4, column = 0,columnspan=2, padx = 3, pady = 3,sticky="WE") 
        btn_input_enter = Button(self.Frame_input, text="ENTER",background ="gray11",foreground = "white") 
        btn_input_enter.grid(row = 4, column = 2, padx = 2, pady = 3,sticky="WE") #pijltjes 
       
#Grote Stop knop
       
       
        btn_stop = Button(self.Frame_input, text="STOP" , command= self.stop, background = "red",foreground = "white")
        btn_stop.config( height = 5, width = 10) 
        btn_stop.grid(row = 1, column = 1, padx = 5, pady = 3, sticky='W') 
       
#pijltjes, A en D
       
        self.Frame_btn_control = Frame(self.Frame_input,background="gray55")
        self.Frame_btn_control.grid(row = 1, column = 2) 
        
        rc_btn_height = 32 
        rc_btn_width = 34 
        
        self.img_left = Image.open('draai.png')
        imgr_left = self.img_left.resize((50, 50),Image.ANTIALIAS)
        self.img_left1 = ImageTk.PhotoImage(imgr_left)
        self.btn_left = Button(self.Frame_btn_control, image=self.img_left1,background ="gray11",foreground = "white") #pijltje omhoog afbeelding #TODO:
        self.btn_left.config( height = rc_btn_height, width = rc_btn_width ) 
        self.btn_left.grid(row = 1, column = 0,padx = 5, pady = 3)

        self.img_down = Image.open('pijl2.png')
        imgr_down = self.img_down.resize((50, 50),Image.ANTIALIAS)
        self.img_down1 = ImageTk.PhotoImage(imgr_down)
        self.btn_down = Button(self.Frame_btn_control, image=self.img_down1,background ="gray11",foreground = "white") #pijltje beneden afbeelding 
        self.btn_down.config( height = rc_btn_height, width = rc_btn_width ) 
        self.btn_down.grid(row = 1, column = 1,padx = 5, pady = 3) 
        
        self.img_up = Image.open('pijl1.png')
        imgr_up = self.img_up.resize((50, 50),Image.ANTIALIAS)
        self.img_up1 = ImageTk.PhotoImage(imgr_up)
        self.btn_up = Button(self.Frame_btn_control, image=self.img_up1,background ="gray11",foreground = "white") #pijltje omhoog afbeelding 
        self.btn_up.config( height = rc_btn_height, width = rc_btn_width ) 
        self.btn_up.grid(row = 0, column = 1 ,padx = 5, pady = 3)
        
        
        self.img_right = Image.open('draai2.png')
        imgr_right = self.img_right.resize((50, 50),Image.ANTIALIAS)
        self.img_right1 = ImageTk.PhotoImage(imgr_right)
        self.btn_right = Button(self.Frame_btn_control, image=self.img_right1,background ="gray11",foreground = "white") #pijltje rechts afbeelding 
        self.btn_right.config( height = rc_btn_height, width = rc_btn_width ) 
        self.btn_right.grid(row = 1, column = 2 ,padx = 5, pady = 3) 
        
        self.img_a = Image.open('pijl1.png')
        imgr_a = self.img_a.resize((50, 50),Image.ANTIALIAS)
        self.img_a1 = ImageTk.PhotoImage(imgr_a)
        self.btn_ascend = Button(self.Frame_btn_control, image=self.img_a1,background ="gray11",foreground = "white") #stijgen
        self.btn_ascend.config( height = rc_btn_height, width = rc_btn_width ) 
        self.btn_ascend.grid(row = 2, column = 0,padx = 5, pady = 3)
        
        self.img_d = Image.open('pijl2.png')
        imgr_d = self.img_d.resize((50, 50),Image.ANTIALIAS)
        self.img_d1 = ImageTk.PhotoImage(imgr_d)
        self.btn_descend = Button(self.Frame_btn_control, image=self.img_d1,background ="gray11",foreground = "white") #dalen
        self.btn_descend.config( height = rc_btn_height, width = rc_btn_width ) 
        self.btn_descend.grid(row = 2, column = 2 ,padx = 5, pady = 3)
        
        #binden GUI-stuurknoppen
        
        self.btn_up.bind("<Button-1>", self.move_forward)
        self.btn_up.bind("<ButtonRelease-1>", self.h_release)
        
        self.btn_down.bind("<Button-1>", self.move_backward)
        self.btn_down.bind("<ButtonRelease-1>", self.h_release)
        
        self.btn_left.bind("<Button-1>", self.turn_left)
        self.btn_left.bind("<ButtonRelease-1>", self.h_release)
        
        self.btn_right.bind("<Button-1>", self.turn_right)
        self.btn_right.bind("<ButtonRelease-1>", self.h_release)
        
        self.btn_ascend.bind("<Button-1>", self.ascend)
        self.btn_ascend.bind("<ButtonRelease-1>", self.v_release)
        
        self.btn_descend.bind("<Button-1>", self.descend)
        self.btn_descend.bind("<ButtonRelease-1>", self.v_release)
        
        #output
        self.Frame_output = Frame(self,background="gray55")
        self.Frame_output.grid(row = 0, column = 1,  sticky='WE') 
        
        #TODO: Frame pictures motors
        
        self.output = ScrolledText(self.Frame_output, undo=True, state='disabled')
        self.output['font'] = ('consolas', '12')
        self.output.config(width = 70, height = 30) 
        self.output.grid(row = 0, column = 0, padx = 5, pady = 5, columnspan = 3,sticky='WE') 
        
        #Grafiek
        self.Frame_visual_view=Frame(self.Frame_output,background="gray55")
        
        self.Frame_motors = Frame(self.Frame_visual_view,background="gray55")
        
        self.motor1 = StringVar()
        self.motor1.set('...')
        
        self.motor2 = StringVar()
        self.motor2.set('...')
        
        self.motor3 = StringVar()
        self.motor3.set('...')
        
        self.lbl_motor1 = Label(self.Frame_motors, textvariable=self.motor1)
        self.lbl_motor1.grid(row = 0, column = 0, padx = 5, pady = 5,sticky='WE') 
        
        self.lbl_motor2 = Label(self.Frame_motors, textvariable=self.motor2)
        self.lbl_motor2.grid(row = 0, column = 1, padx = 5, pady = 5,sticky='WE') 
        
        self.lbl_motor3 = Label(self.Frame_motors, textvariable=self.motor3)
        self.lbl_motor3.grid(row = 0, column = 2, padx = 5, pady = 5,sticky='WE') 
        
        self.Frame_graphview = Frame(self.Frame_visual_view,background="gray55")
        self.Frame_graphview.config(width=800,height = 500)
        self.height_graph = Plotter(self.Frame_graphview,50,3)
        
        self.view_state = 'output'  
        btn_h = Button(self.Frame_output, text="CHANGE VIEW", command = self.invoke_change_view,background ="gray11",foreground = "white") 
        btn_h.config( height = 2, width = 4 ) 
        btn_h.grid(row = 1, column = 0,padx = 5, pady = 3,sticky='WSE')
        
        btn_h = Button(self.Frame_output, text="SHOW H", command = self.invoke_show_height,background ="gray11",foreground = "white") 
        btn_h.config( height = 2, width = 4 ) 
        btn_h.grid(row = 1, column = 1,padx = 5, pady = 3,sticky='WSE')
        
#         self.txt_ct = Text(self.Frame_output, undo=True, state='disabled')
#         self.txt_ct['font'] = ('consolas', '12')
#         self.txt_ct.config(width = 20, height = 1) 
#         self.txt_ct.grid(row = 1, column = 2, padx = 5, pady = 5,sticky='WSE') 

        self.height = StringVar()
        self.height.set('...')
        self.lbl_height = Label(self.Frame_output, textvariable=self.height)
        self.lbl_height.config(width=6)
        self.lbl_height.grid(row = 1, column = 2, padx = 5, pady = 5,sticky='WE')  
        
        
        
        #resizen nog nagaan
        self.grid_columnconfigure(0, weight = 2)
        self.grid_columnconfigure(1,weigh=1)
        self.grid_rowconfigure(0, weight=1)
       
        self.Frame_input.grid_rowconfigure(0, weight=1)
        self.Frame_input.grid_rowconfigure(1, weight=1)
        self.Frame_input.grid_rowconfigure(2, weight=1)
        
        self.Frame_input.grid_columnconfigure(0, weight = 2)
        self.Frame_input.grid_columnconfigure(1,weigh=1)
        
       
    def invoke_change_view(self):
        if self.view_state is 'output':
            self.invoke_change_view_to_graph()
        else: 
            self.invoke_change_view_to_output_text()
            
    def invoke_show_height(self):
        if self.stop_show_height == True:
            self.stop_show_height=False 
            self.show_height()
        else: 
            self.stop_show_height=True
            self.height.set('...')
        
    
    def show_height(self):
        if self.stop_show_height == False:
            height = random.randint(0,11)
            self.height.set(height) 
            self.after(50,self.show_height)
        
    def invoke_change_view_to_graph(self):
        self.Frame_visual_view.grid(row = 0, column = 0, columnspan = 3,sticky='WE') 
        self.Frame_motors.grid(row=1)
        self.Frame_graphview.grid(row=0,column=0)
        self.height_graph.grid(row=0,column=0)        
        self.output.grid_remove()  
        self.show_graphs() 
        self.view_state = 'graph'  
        
    def invoke_change_view_to_output_text(self):
        self.stop_graphs()
        self.Frame_visual_view.grid_remove()
        self.output.grid(row = 0, column = 0, padx = 5, pady = 5, columnspan = 3,sticky='WE')         
        self.view_state = 'output'   
      
    
    def show_graphs(self):
        self.height_graph.stop = False
        self.height_graph.plotter()
       
    def stop_graphs(self):   
        self.height_graph.stop = True    
    
    def invoke_command(self):
        self.Frame_com_menu = Frame(self.Frame_input,background="gray55")
        self.Frame_com_menu.grid(row = 1, column = 0, rowspan = 3, columnspan = 1, sticky='W')    
        
        btn_turn = Button(self.Frame_com_menu, text="TURN", command=self.invoke_turn,background ="gray11",foreground = "white") 
        btn_turn.config( height = 1, width = 7 ) 
        btn_turn.grid(row = 0, column = 0, padx = 5, pady = 3, columnspan = 1, sticky='W')  
        
        btn_move = Button(self.Frame_com_menu, text="MOVE", command=self.invoke_move,background ="gray11",foreground = "white") 
        btn_move.config( height = 1, width = 7 ) 
        btn_move.grid(row = 1, column = 0, padx = 5, pady = 3, columnspan = 1, sticky='W')     
        
        btn_lift = Button(self.Frame_com_menu, text="LIFT", command=self.invoke_lift,background ="gray11",foreground = "white") 
        btn_lift.config( height = 1, width = 7 ) 
        btn_lift.grid(row = 2, column = 0, padx = 5, pady = 3, columnspan = 1, sticky='W')
        
        self.Frame_cmenu.grid_remove()

    def invoke_turn(self):
        self.Frame_turn_menu = Frame(self.Frame_input,background="gray55")
        self.Frame_turn_menu.grid(row = 1, column = 0, rowspan = 3, columnspan = 1, sticky='W')    
        
        entry_turn_input = Entry(self.Frame_turn_menu) 
        entry_turn_input.grid(row = 0, column = 0, padx = 3, pady = 3) 
        
        btn_input_turn_enter = Button(self.Frame_turn_menu, text="ENTER",command=self.invoke_turn_enter,background ="gray11",foreground = "white") 
        btn_input_turn_enter.grid(row = 1, column = 0, padx = 2, pady = 3, columnspan = 3,sticky='W') 
        
        self.Frame_com_menu.grid_remove()

    def invoke_turn_enter(self):
        #stuur string
        self.Frame_turn_menu.grid_remove()
        self.Frame_cmenu.grid(row = 1, column = 0, rowspan = 3, columnspan = 1, sticky='W')
        
    def invoke_move(self):
        self.Frame_move_menu = Frame(self.Frame_input,background="gray55")
        self.Frame_move_menu.grid(row = 1, column = 0, rowspan = 3, columnspan = 1, sticky='W')    
        
        entry_move_input = Entry(self.Frame_move_menu) 
        entry_move_input.grid(row = 0, column = 0, padx = 3, pady = 3) 
        
        btn_input_move_enter = Button(self.Frame_move_menu, text="ENTER",command=self.invoke_move_enter,background ="gray11",foreground = "white") 
        btn_input_move_enter.grid(row = 1, column = 0, padx = 2, pady = 3, columnspan = 3,sticky='W') 
        
        self.Frame_com_menu.grid_remove()

    def invoke_move_enter(self):
        #stuur string
        self.Frame_move_menu.grid_remove()
        self.Frame_cmenu.grid(row = 1, column = 0, rowspan = 3, columnspan = 1, sticky='W')
        
    def invoke_lift(self):
        self.Frame_lift_menu = Frame(self.Frame_input,background="gray55")
        self.Frame_lift_menu.grid(row = 1, column = 0, rowspan = 3, columnspan = 1, sticky='W')    
        
        self.entry_lift_input = Entry(self.Frame_lift_menu) 
        self.entry_lift_input.grid(row = 0, column = 0, padx = 3, pady = 3) 
        
        btn_input_move_enter = Button(self.Frame_lift_menu, text="ENTER",command=self.invoke_lift_enter,background ="gray11",foreground = "white") 
        btn_input_move_enter.grid(row = 1, column = 0, padx = 2, pady = 3, columnspan = 3,sticky='W') 
        
        self.Frame_com_menu.grid_remove()

    def invoke_lift_enter(self):
        #stuur string
        
        height =  self.entry_lift_input.get()
        command = Commands.VertMove(int(height))
        self.queue.put(command)
        
        self.Frame_lift_menu.grid_remove()
        self.Frame_cmenu.grid(row = 1, column = 0, rowspan = 3, columnspan = 1, sticky='W')
        
    def printtest(self,*args):
        print 'check'
   
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #geen elegante schrijfwijze momenteel
    #idee is om bij constructie van GUI ook het controllerobject van de zeppelin
    #mee te geven als argument
    #vervolgens:
    #   def move_zep(self,*args):
    #         self.controller.move(self, 0.1)
    
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
            command= Commands.Move(float('infinity'))
            self.queue.put(command)
            self.flag_btn=True
          
            
    def turn_left(self,*args):
        if self.flag_btn == False:
            command= Commands.Turn(float('-infinity'))
            self.queue.put(command)
            self.flag_btn=True

    def turn_right(self,*args):
        if self.flag_btn == False:
            command= Commands.Turn(float('infinity'))
            self.queue.put(command)
            self.flag_btn=True
        
    def move_backward(self,*args):
        if self.flag_btn == False:
            command= Commands.Move(float('-infinity'))
            self.queue.put(command)
            self.flag_btn=True
        
    def ascend(self,*args):
        if self.flag_btn == False:
            #command= Commands.Ascension(float('infinity')) #Commands.<Stijgen>
            command= Commands.VertMove(100)
            self.queue.put(command)
            self.flag_btn=True
        
    def descend(self,*args):
        if self.flag_btn == False:    
            command= Commands.VertMove(-100)
            self.queue.put(command)
            self.flag_btn=True
        
    def lift(self,height,*args):
        newHeight=self.zeppelin.heigth + height
        print newHeight
        command=Commands.Ascension(newHeight)
        self.queue.put(command)
    
    def move(self,dist,*args):
        command= Commands.Move(dist)
        self.queue.put(command)
    
    def turn(self,degree,*args):
        command= Commands.Turn(degree)
        self.queue.put(command)
    
    def h_stop(self,*args):
        command = Commands.HorStop()
        self.queue.put(command)
        
    def v_stop(self,*args):
      #  command = Commands.VertStop()
        command= Commands.VertMove(0)
        self.queue.put(command)
    
        
    def stop(self,*args):
        command = Commands.Stop()
        self.queue.put(command)
        
# def main(): 
#   
#     foo = 0
#     app = GUI(foo ) 
#     app.parent.mainloop()
# 
# if __name__ == '__main__':
#     main()

GUI(0,0)

