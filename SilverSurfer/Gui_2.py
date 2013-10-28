'''
Created on 21-okt.-2013

@author: Pepino
'''


from Tkinter import * 
from ScrolledText import ScrolledText


class GUI(Frame):
    
     
    def __init__(self, parent): 
        Frame.__init__(self, parent, background="white") 
        self.parent = parent 
        self.initGUI() 
        
        
    def initGUI(self): 
        self.parent.title("Blimp bizkit") #Titel moet door zeppling worden gestuurd 
        self.pack(fill=BOTH, expand=1) 
        
        
        #input
        self.Frame_input = Frame(self,background="white")
        self.Frame_input.grid(row = 0, column = 0, sticky='W') 
        
        
        lbl_image = Label(self.Frame_input, text="Afbeelding") #Text="Afbeelding" moet vervangen worden door image=... 
        lbl_image.config(width = 70, height = 30) 
        lbl_image.grid(row = 0, column = 0, padx = 5, pady = 5, columnspan=2) 
        
        # 3 Menu knoppen 
        
        self.Frame_cmenu = Frame(self.Frame_input,background="white")
        self.Frame_cmenu.grid(row = 1, column = 0,  sticky='W') 
        
        
        menu_btn_width = 7 
        menu_btn_height = 1

      
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
        btn_command.config( height = menu_btn_height, width = 10 ) 
        btn_command.grid(row = 3, column = 0, padx = 5, pady = 3, sticky='W') 
          
            
            
        entry_input = Entry(self.Frame_input) 
        entry_input.grid(row = 4, column = 0, padx = 3, pady = 3,sticky="WE") 
        btn_input_enter = Button(self.Frame_input, text="ENTER") 
        btn_input_enter.grid(row = 4, column = 1, padx = 2, pady = 3,sticky="WE") #pijltjes 
       
       
       #pijltjes, A en D
       
        Frame_btn_control = Frame(self.Frame_input,background="white")
        Frame_btn_control.grid(row = 1, column = 1, rowspan = 3, columnspan = 3) 
        
        rc_btn_height = 2 
        rc_btn_width = 4 
        
        btn_left = Button(Frame_btn_control, text="LEFT") #pijltje omhoog afbeelding 
        btn_left.config( height = rc_btn_height, width = rc_btn_width ) 
        btn_left.grid(row = 1, column = 0,padx = 5, pady = 3)

        btn_down = Button(Frame_btn_control, text="BACK") #pijltje beneden afbeelding 
        btn_down.config( height = rc_btn_height, width = rc_btn_width ) 
        btn_down.grid(row = 1, column = 1,padx = 5, pady = 3) 
        
        btn_up = Button(Frame_btn_control, text="FORW") #pijltje omhoog afbeelding 
        btn_up.config( height = rc_btn_height, width = rc_btn_width ) 
        btn_up.grid(row = 0, column = 1 ,padx = 5, pady = 3)
        
        btn_right = Button(Frame_btn_control, text="RIGHT") #pijltje rechts afbeelding 
        btn_right.config( height = rc_btn_height, width = rc_btn_width ) 
        btn_right.grid(row = 1, column = 2 ,padx = 5, pady = 3) 
        
        btn_ascend = Button(Frame_btn_control, text="A") #stijgen
        btn_ascend.config( height = rc_btn_height, width = rc_btn_width ) 
        btn_ascend.grid(row = 2, column = 0,padx = 5, pady = 3)
        
        btn_descend = Button(Frame_btn_control, text="D") #dalen
        btn_descend.config( height = rc_btn_height, width = rc_btn_width ) 
        btn_descend.grid(row = 2, column = 2 ,padx = 5, pady = 3)
        
        
        
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
    
      
       
     

def main(): 
    root = Tk() 
    root.geometry("1200x650+300+300") 
    app = GUI(root) 
    root.mainloop()

if __name__ == '__main__':
     main()