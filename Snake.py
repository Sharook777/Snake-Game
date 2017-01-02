

# Snake game using tkinter Python (version v.2.1)
# used a more modern python GUI module tkinter
# tested with python 34 20sept2016
# fixed all bugs and works successfully


''' you can control snake using up down left and right arrow keys. objective of
game catch food and score maximum. if the snake collides with boundry or its own
body you will be fail.'''


################################################################################
#########################                          #############################
#########################      AUTHOR SHAROOK      #############################
#########################        SNAKE GAME        #############################
#########################          PUZZLE          #############################
#########################                          #############################
################################################################################

from tkinter import *
import threading
from random import randint
import os.path

class main():
    
    def __init__(self):
        
        self.root=Tk()
        #self.root.geometry('500x500')
        self.root.title('SNAKe G@ME')
        self.root.resizable(0,0)

        self.frame=Frame(self.root,height=50,width=500,bg="black")
        self.newgameb=Button(self.frame,text='New Game',bg="black",fg="white",width=15,height=2,relief='raised',command=self.newgame)
        
        self.label2=Label(self.frame,text='Score',bg="black",fg="white")
        self.label2.pack(side='right')
        self.label1=Label(self.frame,text='High Score',bg="black",fg="white")
        self.label1.pack(side='right')
        self.newgameb.pack(side='left')

        self.frame.pack(expand=YES,fill=X)

        self.frame1=Frame(self.root)

        self.canvas=Canvas(self.frame1,background='black',height=500,width=500)
        self.canvas.focus_set()
        self.canvas.pack(expand=YES,fill=BOTH)

        Width=500
        Height=500
        self.r=Width//25

        self.lastdirection='right'

        self.x1=Width/2-self.r/2             #self.x1
        self.y1=Height/2-self.r/2            #self.x2
        self.x2=Width/2+self.r/2
        self.y2=Height/2+self.r/2

        
        self.newgame()

        self.canvas.bind('<Key>',self.press)

        self.frame1.pack(expand=YES,fill=BOTH)
        self.root.mainloop()

        

    def newgame(self):
        
        self.canvas.delete(ALL)
        self.canvas.create_text(self.x1,self.y1,fill='white',font=50,text='Welcome to SNAKE game'+'\n        Beat Highscore'+'\nClick mouse button to start',tag='welcometext')

        global head
        head=self.canvas.create_rectangle(0,self.y1,20,self.y2,outline='#dbf',fill='red',tag='head',stipple='gray50')
        rect2=self.canvas.create_rectangle(0,self.y1,20,self.y2,outline='#dbf',fill='green',tag='rect2',stipple='gray50')
        rect3=self.canvas.create_rectangle(0,self.y1,20,self.y2,outline='#dbf',fill='green',tag='rect3',stipple='gray50')

        self.direction='right'
        self.rectangles=['head','rect2','rect3']

        self.score=0


        if(os.path.isfile('highscore.txt')):
            storefile=open('highscore.txt','r')
            #print(storefile)
            self.highscore=int(storefile.read())
            #print(self.highscore)
            storefile.close()
        else:
            self.highscore=0
            
        self.label1['text']='Highscore: '+str(self.highscore)
        self.label2['text']='Score: '+'0'

        self.canvas.bind('<Button-1>',self.start)

        

    def start(self,event=None):
        w=self.r

        self.canvas.unbind('<Button-1>')
        
        self.canvas.delete('welcometext')
        self.canvas.move('head',w,0)
        self.canvas.move('head',w,0)
        
        self.canvas.move('rect2',w,0)

        self.movethread()
        self.makefud()

        

    def press(self,event):
       
        if(event.keycode==37):
            self.direction='left'
        elif(event.keycode==38):
            self.direction='up'
        elif(event.keycode==39):
            self.direction='right'
        elif(event.keycode==40):
            self.direction='down'
        


    def movethread(self):       # create thread
        threading.Thread(target=self.move).start()


    def move(self):
        w=self.r
        x,y=w,0
        
        global lastdirection
        
        lock=threading.Lock()
        lock.acquire()
        
        while(True):
            
            #lock=threading.Lock()
            #lock.acquire()
            
            rect=self.rectangles.pop()
            #print(rect)
            
            self.firstcoords=self.canvas.coords(head)
            
            self.first=self.canvas.coords(rect)
            
            if(self.direction=='left'and self.lastdirection!='right'):
                self.canvas.move('head',-w,0)
                x,y=-w,0
                self.lastdirection='left'
                
            elif(self.direction=='down'and self.lastdirection!='up'):
                self.canvas.move('head',0,w)
                x,y=0,w
                self.lastdirection='down'
                
            elif(self.direction=='right'and self.lastdirection!='left'):
                self.canvas.move('head',w,0)
                x,y=w,0
                self.lastdirection='right'
                
            elif(self.direction=='up'and self.lastdirection!='down'):
                self.canvas.move('head',0,-w)
                x,y=0,-w
                self.lastdirection='up'
                
            else:
                self.canvas.move('head',x,y)
    
            u=self.firstcoords[0]-self.first[0]
            v=self.firstcoords[1]-self.first[1]
           
            self.canvas.move(self.canvas.gettags(rect),u,v)

            self.rectangles.insert(1,rect)
            self.canvas.after(80)
            #lock.release()

            self.collision(x,y,self.firstcoords)
            
            stat=self.boundry()
            
            if(stat==True):
                self.canvas.create_text(self.x1,self.x2-20,fill='white',font=50,text='GAME OVER')
                self.canvas.create_text(self.x1,self.x2+20,fill='white',font=50,text='Score: '+str(self.score))
                if(self.score>self.highscore):
                    scorefile=open('highscore.txt','w')
                    scorefile.write(str(self.score))
                    scorefile.close()
                break

            
        lock.release()



    def makefud(self):
    
        #q=random.random()      # gnerate random number in between 0.0 to 1.0

        
        global dotx,doty
    
        self.canvas.delete('dot')
        q=randint(20,480)
        w=randint(20,480)
    
        dotx=q
        doty=w
        dotx,doty=int(dotx),int(doty)
    
        '''c,d=dotx%20,doty%20
        dotx,doty=dotx+c,doty+d
        print(dotx,doty)'''
    
    
        self.dot=self.canvas.create_oval(dotx,doty,dotx+self.r,doty+self.r,fill='blue',tag='dot')
        


    def boundry(self):
    
        coord=self.canvas.coords(head)
        if(coord[0]+20==0 or coord[2]-20==500 or coord[1]+20==0 or coord[3]-20==500 ):
            return True
        
        front=self.canvas.coords(self.canvas.gettags(head))
        overlap2=self.canvas.find_overlapping(front[0]+10,front[1]+10,front[2]-10,front[3]-10)
        
        if(len(overlap2)>=2):
            if(self.dot not in overlap2):
                return True
        return False



    def grow(self,x,y):
    
        w=self.r
    
        lock=threading.Lock()
        lock.acquire()
    
        tail=self.canvas.coords(self.rectangles[((len(self.rectangles))-1)])
        thistag='rect'+str(len(self.rectangles)+1)
    
        x11=int(tail[0])+x
        y11=int(tail[1])+y
        x22=int(tail[2])+x
        y22=int(tail[3])+y
    
        rect=self.canvas.create_rectangle(x11,y11,x22,y22,outline='#dbf',fill='green',tag=thistag,stipple='gray50')
        self.rectangles.append(thistag)
    
        lock.release()


        

    def collision(self,x,y,front):

        global score
    
        lock=threading.Lock()
        lock.acquire()
    
        #front=canvas.coords(canvas.gettags(head))
        
        print(front)
        
        overlap=self.canvas.find_overlapping(front[0],front[1],front[2],front[3])
    
        for item in overlap:
            if(item==self.dot):
                self.makefud()
                self.grow(x,y)
                self.score+=100
                self.label2['text']='Score: '+str(self.score)
                
        lock.release()

    

        
main()
