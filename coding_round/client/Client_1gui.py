import tkSimpleDialog
from Tkinter import *
import tkFont
import Tkinter as tk2
from tkFileDialog import askopenfilename
import tkMessageBox
import socket,time,thread
import sys
import getpass,os
import datetime
import tkFileDialog
import tkMessageBox
host='172.16.82.61'
class App:
  
    def __init__(self, master):
	frame = Frame(master, width=1000, height=600, bg="lightgreen",  colormap="new")
	frame.pack()
	master.title("LOGIN SCREEN")

	abc=tkFont.Font(family="Helvetica", size=40 )	
	abc1=tkFont.Font(family="Helvetica", size=16 )
	abc2=tkFont.Font(family="Helvetica", size=20 )
	abc3=tkFont.Font(family="Helvetica", size=15 )

	l=Label(frame, text="CODE", font=abc, bg="lightgreen")
        l.pack()
	l.place(relx=0.45, rely=0.15, anchor=CENTER)
	l=Label(frame, text="ACHARYA", font=abc, bg="lightgreen")	
	l.pack()
	
	l.place(relx=0.75, rely=0.15, anchor=CENTER)
	l=Label(frame, text="Hand tool for teachers", font=abc3, bg="lightgreen")
        l.pack()
	l.place(relx=0.60, rely=0.345, anchor=CENTER)
	l1=Label(frame, text="Username:", font=abc2, bg="lightgreen")
	l1.pack()
	l1.place(relx=0.2, rely=0.57, anchor=CENTER)
        l2=Label(frame, text="Password:",bg="lightgreen", font=abc2)
	l2.pack()
	l2.place(relx=0.2, rely=0.67, anchor=CENTER)

        self.e1 = Entry(frame, font=abc2, fg="black")
	self.e1.pack(side=RIGHT,padx=15, pady=15)
	self.e1.place(relx=0.6, rely=0.57, anchor=CENTER)
        self.e2 = Entry(frame,show="*", font=abc2)
	self.e2.place(relx=0.6, rely=0.67, anchor=CENTER)
       
	photo=PhotoImage(file="jiit.gif")
	ph=Label(frame,image=photo , bg="lightgreen")
	ph.photo=photo
	ph.pack()
	ph.place(relx=0.03,rely=0.03)
	        
	button1 = self.button = Button(frame, text="LOGIN",font=abc1, command=self.login)
        button1.pack(side=LEFT,padx=15, pady=55)
	button1.place(relx=0.3, rely=0.83, anchor=CENTER)		
	button2=self.button = Button(frame, text="QUIT", font=abc1, command=frame.quit)
	button2.pack(side=LEFT)
	button2.place(relx=0.7, rely=0.83, anchor=CENTER)			
        
	frame.propagate(False)		
    def login(self):
	username=self.e1.get()	
	password=self.e2.get()

	s.send(username)
	s.recv(1)
	s.send(password)
	s.recv(1)
	x=s.recv(30)
	s.send('1')
	if(x!="0"):
		tkMessageBox.showinfo("ERROR", x)
		sys.exit(0) 
	endtime=s.recv(20)
	s.send('0')


	root.destroy()
	global root1	
	root1=Tk()	
	app = App1(root1,username,password)


class App1:
	
    def __init__(self, master,un,nm):
        self.un=un
        self.nm=nm
	master.title("PARTICIPANT PANEL")
	frame = Frame(master, width=1000, height=600, bg="lightgreen",  colormap="new")
	frame.pack()
	abc=tkFont.Font(family="Helvetica", size=40 )	
	abc1=tkFont.Font(family="Helvetica", size=13 )
	abc2=tkFont.Font(family="Helvetica", size=20 )
	abc3=tkFont.Font(family="Helvetica", size=15 )
        
	l=Label(frame, text="Code", font=abc, bg="lightgreen")
        l.pack()
	l.place(relx=0.45, rely=0.15, anchor=CENTER)
	l=Label(frame, text="Acharya", font=abc, bg="lightgreen")	
	l.pack()
	
	l.place(relx=0.75, rely=0.15, anchor=CENTER)
	l=Label(frame, text="Hand tool for teachers", font=abc3, bg="lightgreen")
        l.pack()
	l.place(relx=0.60, rely=0.345, anchor=CENTER)
	photo=PhotoImage(file="2.gif")
	ph=Label(frame,image=photo, bg="lightgreen")
	ph.photo=photo
	ph.pack()
	ph.place(relx=0.03,rely=0.10)
        l=Label(frame, text= str("Welcome  " + self.nm + " ( "+ self.un+ " )"), font=abc2, bg="lightgreen")
        l.pack()
	l.place(relx=0.1, rely=0.445)


	
	button1 = self.button = Button(frame, text="           SUBMIT           ",font=abc1, command=self.submit)
        button1.pack(side=LEFT,padx=15, pady=55)
	button1.place(relx=0.30, rely=0.55, anchor=CENTER)		
	button2=self.button = Button(frame, text="       CHECK TIME        ", font=abc1, command=self.checktime)
	button2.pack(side=LEFT,padx=15, pady=55)
	button2.place(relx=0.70, rely=0.75, anchor=CENTER)			
	button1 = self.button = Button(frame, text="    PREVIOUS RUNS    ",font=abc1, command=self.previousruns)
        button1.pack(side=LEFT,padx=15, pady=55)
	button1.place(relx=0.30, rely=0.75, anchor=CENTER)		
	button1 = self.button = Button(frame, text="CHECK SCOREBOARD",font=abc1, command=self.checkscoreboard)
        button1.pack(side=LEFT,padx=15, pady=55)
	button1.place(relx=0.70, rely=0.55, anchor=CENTER)
	button3 = self.button = Button(frame, text="Download Labtest",font=abc1, command=self.downloadProblem)
        button3.pack(side=LEFT,padx=15, pady=55)
	button3.place(relx=0.50, rely=0.75, anchor=CENTER)				
	button1 = self.button = Button(frame, text="EXIT",font=abc1, command=self.quitcontest)
        button1.pack(side=LEFT,padx=15, pady=55)
	button1.place(relx=0.50, rely=0.95, anchor=CENTER)
	button1 = self.button = Button(frame, text="           view ques           ",font=abc1, command=self.view)
        button1.pack(side=LEFT,padx=15, pady=55)
	button1.place(relx=0.50, rely=0.55, anchor=CENTER)		
	
	frame.propagate(False)
    def view(self):
        #root1.destroy()
        #global root3
        #root3=Tk()
        #app = MyText(root3)
        #root3.mainloop()

        tk = Tk()
        tk.title('Text Reader App')
        atext = MyText(tk)
        atext.pack()
        open_button = Button(tk, text="Open File",activeforeground='blue',command=atext.set_from_file)
        #close_button = Button(tk, text="close",activeforeground='blue',command=atext.abc)
        #close_button.pack()
        open_button.pack()
        tk.mainloop()		
    def submit(self):
	s.send('1')
	root1.destroy()
	global root2	
	root2=Tk()	
	app = App2(root2,self.nm)
    def checkscoreboard(self):
	s.send('2')
	scoreresult=s.recv(1024)
	s.send('1')
	tkMessageBox.showinfo("SCOREBOARD", scoreresult)
	#root1.destroy()
    def previousruns(self):
	s.send('3')
	scoreresult=s.recv(1024)
	s.send('1')
	tkMessageBox.showinfo("PREVIOUS RUNS", scoreresult)
	#root1.destroy()
    def checktime(self):
	s.send('4')
	scoreresult=s.recv(1024)
	s.send('1')
	tkMessageBox.showinfo("TIME LEFT", scoreresult)
	#root1.destroy()
    def quitcontest(self):
	s.send('5')
	root1.destroy()
    def downloadProblem(self):
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((host, 50100))
	k = ' '
	size = 1024
	results = 'labtest'
	#client_socket.send('1')	    
	client_socket.send(results)
	#size = client_socket.recv(1024)
	#size = int(size)
	#print "The file size is - ",size," bytes"
	#size = size*2
	strng = client_socket.recv(1024)
	print "\nThe contents of that file - "
	print strng
	temp=results
	fp = open(temp,'w')
	fp.write(strng)
	fp.close()
	
	

class App2:
    filename=''
    def __init__(self, master,nn):
        self.nn=nn
	master.title("SUBMIT SOLUTION")
	frame = Frame(master, width=1000, height=600, bg="lightgreen",  colormap="new")
	frame.pack()
	
	abc=tkFont.Font(family="Helvetica", size=40 )	
	abc1=tkFont.Font(family="Helvetica", size=13 )
	abc2=tkFont.Font(family="Helvetica", size=20 )
	abc3=tkFont.Font(family="Helvetica", size=15 )

	l=Label(frame, text="CODE", font=abc, bg="lightgreen")
        l.pack()
	l.place(relx=0.45, rely=0.15, anchor=CENTER)
	l=Label(frame, text="ACHARYA", font=abc, bg="lightgreen")	
	l.pack()
	
	l.place(relx=0.75, rely=0.15, anchor=CENTER)
	l=Label(frame, text="Hand Tool For Teachers", font=abc3, bg="lightgreen")
        l.pack()
	l.place(relx=0.60, rely=0.345, anchor=CENTER)
	photo1=PhotoImage(file="2.gif")
	ph=Label(frame,image=photo1, bg="lightgreen")
	ph.photo=photo1
	ph.pack()
	ph.place(relx=0.03,rely=0.10)
        l=Label(frame, text= str("      " + self.nn + "  your  SUBMITTING PANEL"), font=abc2, bg="lightgreen")
        l.pack()
	l.place(relx=0.1, rely=0.445 )
	global var2
	var2 = tk2.StringVar(frame)
	var2.set('SELECT QUESTION')
	queslist=s.recv(1024)
	s.send('0')

	choices = queslist.split('\n')
	option = tk2.OptionMenu(frame, var2, *choices)
	option.config(font=abc1)
	option.pack(side='left', padx=10, pady=10)
	option.place(relx=0.60, rely=0.65, anchor=CENTER)
	global var	
	var = tk2.StringVar(frame)
	var.set('SELECT LANGUAGE')
 	choices = ['py', 'c', 'cpp', 'java']
	option = tk2.OptionMenu(frame, var, *choices)
	option.config(font=abc1)
	option.pack(side='left', padx=10, pady=10)
	option.place(relx=0.25, rely=0.65, anchor=CENTER)
	button1 = self.button = Button(frame, text="CHOOSE FILE",font=abc1, command=self.main)
        button1.pack(side=LEFT,padx=15, pady=55)
	button1.place(relx=0.60, rely=0.85, anchor=CENTER)	
	button1 = self.button = Button(frame, text="SUBMIT SOLUTION",font=abc1, command=self.select)
        button1.pack(side=LEFT,padx=15, pady=55)
	button1.place(relx=0.25, rely=0.85, anchor=CENTER)

	frame.propagate(False)

    def select(self):
	global filename
	#ques = "value is %s" % var.get()
	ques = var2.get() 	
	#sf = "value is %s" % var.get()
	ext = var.get()
	s.send(ques)
	x=s.recv(1)
	s.send(ext)
	x=s.recv(1)
	s.send(str(filename.split('/')[-1]))
	x=s.recv(1)
	f=open (filename, "rb") 
	data=f.read()
	f.close()
	s.send(str(len(data)))
	s.recv(1)
	s.send(data)
	result=s.recv(1024)
	s.send('0')
	tkMessageBox.showinfo("RESULT", result)
	root2.destroy()

    def main(self):
	global filename		
	filename = askopenfilename(filetypes=[("python files","*.py"),("c files","*.c"),("cpp files","*.cpp"),("java files","*.java")])
#	root2=Tk()	
#	app = App2(root2)
	



port=50017
s=socket.socket()
try:
	s.connect((host,port))
except:
	print 'Server down'
	sys.exit(0)
root = Tk()
app = App(root)
class MyText(Frame):
    def __init__(self, parent=None, *args, **kwargs):
        Frame.__init__(self, parent)
        self.pack()
        self.text = Text(self, *args, **kwargs)
        self.text.config(background='white')
        self.text.pack(expand=YES, fill=BOTH)
    def get(self):
        return self.text.get(1.0,"%s-1c" % END)
    def set(self, astr):
        self.text.delete(1.0, END)
        self.text.insert(INSERT, astr)
    def set_from_file(self):
        afilename = tkFileDialog.askopenfilename()
        if afilename:
            try:
                afile = open(afilename)
                self.set(afile.read())
                afile.close()
            except Exception, e:
                tkMessageBox.showwarning("File Problem",
                "Couldn't read file '%s': %s" % (afilename, str(e)))
    #def abc(self):
     #   sys.exit(0)

def main():
    tk = Tk()
    tk.title('Lab test question')
    atext = MyText(tk)
    atext.pack()
    open_button = Button(tk, text="Open File",activeforeground='blue',command=atext.set_from_file)
    open_button.pack()
    tk.mainloop()







root.mainloop()
