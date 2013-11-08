


from Tkinter import * 
from ScrolledText import ScrolledText
import Commands
import Queue
import matplotlib.pyplot as pp


class GUI(Frame):
    
     
    def __init__(self, queue,zeppelin): 
        self.parent = Tk() 
        self.parent.geometry("1300x650+300+300") 
        Frame.__init__(self, self.parent, background="white") 
        self.zeppelin=zeppelin
        self.initGUI() 
        self.queue=queue
        self.parent.mainloop()
        
        
    def initGUI(self): 
        self.parent.title("Blimp bizkit") #Titel moet door zeppling worden gestuurd 
        self.pack(fill=BOTH, expand=1) 
        
        #flag_btn init op false
        self.flag_btn = False
        
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
        self.Frame_input = Frame(self,background="white")
        self.Frame_input.grid(row = 0, column = 0, sticky='W') 
        
        
        lbl_image = Label(self.Frame_input, text="Afbeelding") #Text="Afbeelding" moet vervangen worden door image=... 
        lbl_image.config(width = 70, height = 30) 
        lbl_image.grid(row = 0, column = 0, padx = 5, pady = 5, columnspan=3) 
        
        # 3 Menu knoppen 
        menu_btn_width = 7 
        menu_btn_height = 1
        
        self.Frame_cmenu = Frame(self.Frame_input,background="white")
        self.Frame_cmenu.config(width= 1)
        self.Frame_cmenu.grid(row = 1, column = 0,  sticky='W') 

      
        btn_read_qr = Button(self.Frame_cmenu, text="READ QR") 
        btn_read_qr.config( height = menu_btn_height, width = menu_btn_width ) 
        btn_read_qr.grid(row = 0, column = 0, padx = 5, pady = 3, columnspan = 1, sticky='W') 
        
        btn_record = Button(self.Frame_cmenu, text="RECORD") 
        btn_record.config( height = menu_btn_height, width = menu_btn_width ) 
        btn_record.grid(row = 1, column = 0, padx = 5, pady = 3, columnspan = 1,sticky='W') 
        
        btn_pic = Button(self.Frame_cmenu, text="TAKE PIC") 
        btn_pic.config( height = menu_btn_height, width = menu_btn_width ) 
        btn_pic.grid(row = 2, column = 0, padx = 5, pady = 3, columnspan = 1,sticky='W') #Manual input 
       
       
        btn_command = Button(self.Frame_cmenu, text="COMMAND" , command= self.invoke_command )
        btn_command.config( height = menu_btn_height, width = menu_btn_width + 3 ) 
        btn_command.grid(row = 3, column = 0, padx = 5, pady = 3, sticky='W') 
          
            
            
        entry_input = Entry(self.Frame_input) 
        entry_input.config( width = 1 )
        entry_input.grid(row = 4, column = 0,columnspan=2, padx = 3, pady = 3,sticky="WE") 
        btn_input_enter = Button(self.Frame_input, text="ENTER") 
        btn_input_enter.grid(row = 4, column = 2, padx = 2, pady = 3,sticky="WE") #pijltjes 
       
#Grote Stop knop
       
       
        btn_stop = Button(self.Frame_input, text="STOP" , command= self.stop )
        btn_stop.config( height = 5, width = 10) 
        btn_stop.grid(row = 1, column = 1, padx = 5, pady = 3, sticky='W') 
       
#pijltjes, A en D
       
        self.Frame_btn_control = Frame(self.Frame_input,background="white")
        self.Frame_btn_control.grid(row = 1, column = 2, rowspan = 3, columnspan = 3) 
        
        rc_btn_height = 2 
        rc_btn_width = 4 
        
        self.btn_left = Button(self.Frame_btn_control, text="LEFT") #pijltje omhoog afbeelding 
        self.btn_left.config( height = rc_btn_height, width = rc_btn_width ) 
        self.btn_left.grid(row = 1, column = 0,padx = 5, pady = 3)

        self.btn_down = Button(self.Frame_btn_control, text="BACK") #pijltje beneden afbeelding 
        self.btn_down.config( height = rc_btn_height, width = rc_btn_width ) 
        self.btn_down.grid(row = 1, column = 1,padx = 5, pady = 3) 
        
        self.btn_up = Button(self.Frame_btn_control, text="FORW") #pijltje omhoog afbeelding 
        self.btn_up.config( height = rc_btn_height, width = rc_btn_width ) 
        self.btn_up.grid(row = 0, column = 1 ,padx = 5, pady = 3)
        
        
        
        self.btn_right = Button(self.Frame_btn_control, text="RIGHT") #pijltje rechts afbeelding 
        self.btn_right.config( height = rc_btn_height, width = rc_btn_width ) 
        self.btn_right.grid(row = 1, column = 2 ,padx = 5, pady = 3) 
        
        self.btn_ascend = Button(self.Frame_btn_control, text="A") #stijgen
        self.btn_ascend.config( height = rc_btn_height, width = rc_btn_width ) 
        self.btn_ascend.grid(row = 2, column = 0,padx = 5, pady = 3)
        
        self.btn_descend = Button(self.Frame_btn_control, text="D") #dalen
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
        Frame_output = Frame(self,background="white")
        Frame_output.grid(row = 0, column = 1,  sticky='WE') 
        
        output = ScrolledText(Frame_output, undo=True, state='disabled')
        output['font'] = ('consolas', '12')
        output.config(width = 70, height = 30) 
        output.grid(row = 0, column = 0, padx = 5, pady = 5, columnspan = 2,sticky='WE') 
        
        btn_h = Button(Frame_output, text="H") 
        btn_h.config( height = rc_btn_height, width = rc_btn_width ) 
        btn_h.grid(row = 1, column = 0,padx = 5, pady = 3,sticky='WE')
        
        txt_ct = Text(Frame_output, undo=True, state='disabled')
        txt_ct['font'] = ('consolas', '12')
        txt_ct.config(width = 20, height = 1) 
        txt_ct.grid(row = 1, column = 1, padx = 5, pady = 5,sticky='WE') 
        
        
        
        #resizen nog nagaan
        self.grid_columnconfigure(0, weight = 2)
        self.grid_columnconfigure(1,weigh=1)
        self.grid_rowconfigure(0, weight=1)
       
        self.Frame_input.grid_rowconfigure(0, weight=1)
        self.Frame_input.grid_rowconfigure(1, weight=1)
        self.Frame_input.grid_rowconfigure(2, weight=1)
        
        self.Frame_input.grid_columnconfigure(0, weight = 2)
        self.Frame_input.grid_columnconfigure(1,weigh=1)
        
       
        
    
    def invoke_command(self):
        self.Frame_com_menu = Frame(self.Frame_input,background="white")
        self.Frame_com_menu.grid(row = 1, column = 0, rowspan = 3, columnspan = 1, sticky='W')    
        
        btn_turn = Button(self.Frame_com_menu, text="TURN", command=self.invoke_turn) 
        btn_turn.config( height = 1, width = 7 ) 
        btn_turn.grid(row = 0, column = 0, padx = 5, pady = 3, columnspan = 1, sticky='W')  
        
        btn_move = Button(self.Frame_com_menu, text="MOVE", command=self.invoke_move) 
        btn_move.config( height = 1, width = 7 ) 
        btn_move.grid(row = 1, column = 0, padx = 5, pady = 3, columnspan = 1, sticky='W')     
        
        btn_lift = Button(self.Frame_com_menu, text="LIFT", command=self.invoke_lift) 
        btn_lift.config( height = 1, width = 7 ) 
        btn_lift.grid(row = 2, column = 0, padx = 5, pady = 3, columnspan = 1, sticky='W')
        
        self.Frame_cmenu.grid_remove()

    def invoke_turn(self):
        self.Frame_turn_menu = Frame(self.Frame_input,background="white")
        self.Frame_turn_menu.grid(row = 1, column = 0, rowspan = 3, columnspan = 1, sticky='W')    
        
        entry_turn_input = Entry(self.Frame_turn_menu) 
        entry_turn_input.grid(row = 0, column = 0, padx = 3, pady = 3) 
        
        btn_input_turn_enter = Button(self.Frame_turn_menu, text="ENTER",command=self.invoke_turn_enter) 
        btn_input_turn_enter.grid(row = 1, column = 0, padx = 2, pady = 3, columnspan = 3,sticky='W') 
        
        self.Frame_com_menu.grid_remove()

    def invoke_turn_enter(self):
        #stuur string
        self.Frame_turn_menu.grid_remove()
        self.Frame_cmenu.grid(row = 1, column = 0, rowspan = 3, columnspan = 1, sticky='W')
        
    def invoke_move(self):
        self.Frame_move_menu = Frame(self.Frame_input,background="white")
        self.Frame_move_menu.grid(row = 1, column = 0, rowspan = 3, columnspan = 1, sticky='W')    
        
        entry_move_input = Entry(self.Frame_move_menu) 
        entry_move_input.grid(row = 0, column = 0, padx = 3, pady = 3) 
        
        btn_input_move_enter = Button(self.Frame_move_menu, text="ENTER",command=self.invoke_move_enter) 
        btn_input_move_enter.grid(row = 1, column = 0, padx = 2, pady = 3, columnspan = 3,sticky='W') 
        
        self.Frame_com_menu.grid_remove()

    def invoke_move_enter(self):
        #stuur string
        self.Frame_move_menu.grid_remove()
        self.Frame_cmenu.grid(row = 1, column = 0, rowspan = 3, columnspan = 1, sticky='W')
        
    def invoke_lift(self):
        self.Frame_lift_menu = Frame(self.Frame_input,background="white")
        self.Frame_lift_menu.grid(row = 1, column = 0, rowspan = 3, columnspan = 1, sticky='W')    
        
        entry_lift_input = Entry(self.Frame_lift_menu) 
        entry_lift_input.grid(row = 0, column = 0, padx = 3, pady = 3) 
        
        btn_input_move_enter = Button(self.Frame_lift_menu, text="ENTER",command=self.invoke_lift_enter) 
        btn_input_move_enter.grid(row = 1, column = 0, padx = 2, pady = 3, columnspan = 3,sticky='W') 
        
        self.Frame_com_menu.grid_remove()

    def invoke_lift_enter(self):
        #stuur string
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
            command= Commands.Ascension(float('infinity')) #Commands.<Stijgen>
            self.queue.put(command)
            self.flag_btn=True
        
    def descend(self,*args):
        if self.flag_btn == False:    
            command= Commands.Ascension(float('-infinity'))
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
        command = Commands.VertStop()
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


Gui = GUI(0,0)

