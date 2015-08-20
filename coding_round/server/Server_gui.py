import tkSimpleDialog
from Tkinter import *
import Tkinter as tk
import tkFont
import socket,thread
import sys
import MySQLdb
import getpass
import os
import filecmp
import commands
import datetime
import time
import tkMessageBox
import re


def conteststart():
	global starttime,contestflag,endtime,contesttimesec,s
	contestflag=1
	host=''
	port=50017
	s.bind((host,port))
	s.listen(5)
	starttime=datetime.datetime.now().replace(microsecond=0)
	endtime=starttime + datetime.timedelta(seconds=contesttimesec)
	print 'Contest starts at: ',starttime,' and will end at:',endtime
	

def handleclient(conn,addr):
    global subid,starttime,endtime
    db = MySQLdb.connect("localhost","root","","minor",3306,"/opt/lampp/var/mysql/mysql.sock" )
    cursor = db.cursor()
    username=conn.recv(20)
    conn.send('0')
    password=conn.recv(20)
    conn.send('0')
    sql = "SELECT * FROM login"
    flag=0
    try:
       cursor.execute(sql)
       results = cursor.fetchall()
       for row in results:
    	    if( row[0]==username and row[1]==password and row[2]=='user' ):
		    flag=1
    except:
       conn.send("Error: unable to fetch data.")
       sys.exit(0)
    if(flag==0):
       conn.send("Wrong Credentials. ")
       sys.exit(0)
    conn.send("0")
    conn.recv(1)
    try:
        cursor.execute("update loggedin set status='YES' where username='"+username+"'")
        cursor.execute("update loggedin set ip='"+str(addr[0])+"' where username='"+username+"'")
	db.commit()
    except:
	db.rollback()
    print username+' connected from '+str(addr)
    conn.send(str(endtime))
    conn.recv(1)
    while(1):
	    choice=conn.recv(1)
	    time1=datetime.datetime.now().replace(microsecond=0)
	    if(time1>endtime or choice=='5'):
		    break
	    if(choice=='1'):
		    subid=subid+1


		    sql = "SELECT * FROM questions"
		    cursor.execute(sql)
		    results = cursor.fetchall()
		    queslist=''
		    for row in results:
		    	queslist=queslist+row[0]+"\n"
		    queslist=queslist.strip()
		    conn.send(queslist)
		    conn.recv(1)	    



		    quesname=conn.recv(20)
		    sql = "SELECT * FROM questions"
		    flag=0
		    try:
		       cursor.execute(sql)
		       results = cursor.fetchall()
		       for row in results:
		    	    if( row[0]==quesname):
				    flag=1
		    except:
		       x=conn.send("1")
		       sys.exit(0)
		    if(flag==0):
		       conn.send("1")
		       sys.exit(0)
		    x=conn.send("0")

		    fileext=conn.recv(20)
		    x=conn.send("0")
		    filename=conn.recv(20)
		    filename1=filename
		    x=conn.send("0")
		    filename="files/"+str(subid)+filename1
		    filename2="files/"+filename1
		    if(fileext!='java'):
		    	f=open(filename,"w")
		    else:
		    	f=open(filename2,"w")
		    data1=conn.recv(5)
		    conn.send('0')
		    filedata=conn.recv(int(data1))
		   
		    f.write(filedata)
		    f.close()
		    status=0
		    error=""
		    if(fileext=='c'):
			    x = commands.getstatusoutput('gcc '+filename)
			    if(x[0]==0):
				    y = commands.getstatusoutput('./a.out <io/'+quesname+'input.txt >io/'+quesname+'output.txt')
				    if(y[0]!=0):
					    status='RUNTIME ERROR';
					    for j in y:
						   error=error+str(j)+"\n"
				    else:
					    if (filecmp.cmp('io/'+quesname+'output.txt', 'io/'+quesname+'output_server.txt')==True):
					           status='ACCEPTED';
					    else:
						   status='WRONG ANSWER';
			    else: 
				    status='COMPILATION ERROR';
				    for i in x:
					    error=error+str(i)+"\n"
		    elif(fileext=='cpp'):
			    x = commands.getstatusoutput('g++ '+filename)
			    if(x[0]==0):
				    y = commands.getstatusoutput('./a.out <io/'+quesname+'input.txt >io/'+quesname+'output.txt')
				    if(y[0]!=0):
					    status='RUNTIME ERROR';
					    for j in y:
						   error=error+str(j)+"\n"
				    else:
					    if (filecmp.cmp('io/'+quesname+'output.txt', 'io/'+quesname+'output_server.txt')==True):
					           status='ACCEPTED';
					    else:
						   status='WRONG ANSWER';
			    else:
				    status='COMPILATION ERROR';
				    for i in x:
					    error=error+str(i)+"\n"
		    elif(fileext=='java'):
			    x = commands.getstatusoutput('javac '+filename2)
			    if(x[0]==0):
				    y = commands.getstatusoutput('java -cp files Main <io/'+quesname+'input.txt >io/'+quesname+'output.txt')
				    if(y[0]!=0):
					    status='RUNTIME ERROR';
					    for j in y:
						   error=error+str(j)+"\n"
				    else:
					    if (filecmp.cmp('io/'+quesname+'output.txt', 'io/'+quesname+'output_server.txt')==True):
					           status='ACCEPTED';
					    else:
						   status='WRONG ANSWER';
			    else:
				    status='COMPILATION ERROR';
				    for i in x:
					    error=error+str(i)+"\n"
		    elif(fileext=='py'):
				    y = commands.getstatusoutput('python '+filename+' <io/'+quesname+'input.txt >io/'+quesname+'output.txt')
				    if(y[0]!=0):
					    status='PYTHON ERROR';
					    for j in y:
						   error=error+str(j)+"\n"
				    else:
					    if (filecmp.cmp('io/'+quesname+'output.txt', 'io/'+quesname+'output_server.txt')==True):
					           status='ACCEPTED';
					    else:
						   status='WRONG ANSWER';
		    subtime=datetime.datetime.now().replace(microsecond=0)
		    print "user "+username+" submitted for question "+quesname+" in "+fileext+" at "+str(subtime)+". Result: "+status
		    error=error.replace(filename,filename1)
		    conn.send(status+"\n"+error)
		    conn.recv(1)
		    l = str(subtime-starttime).split(':')
		    time= int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])
		    try:
			cursor.execute("insert into submission values("+str(subid)+",'"+username+"','"+quesname+"','"+fileext+"','"+status+"','"+str(subtime)+"','"+filename+"')")
			if(status=='ACCEPTED'):
			        sql_q="select* from accepted";
			        cursor.execute(sql_q);
			        ans = cursor.fetchall()
			        c=0;
				for row in ans:
					if(row[0]==username and row[1]==quesname):
						print 'You have already submited this question'
						c=1;
					else:
					        c=1;
						cursor.execute("insert into accepted values('"+username+"','"+quesname+"','"+str(subtime)+"')")
						cursor.execute("update score set score=score+100 where username='"+username+"'")
						cursor.execute("update score set time=time+"+str(time)+" where username='"+username+"'")
			if(c==0):
				cursor.execute("insert into accepted values('"+username+"','"+quesname+"','"+str(subtime)+"')")
				cursor.execute("update score set score=score+100 where username='"+username+"'")
				cursor.execute("update score set time=time+"+str(time)+" where username='"+username+"'")
				c=1;
			if(status=='WRONG ANSWER'):
				cursor.execute("update score set score=score-50 where username='"+username+"'")
				cursor.execute("update score set time=time+"+str(time)+" where username='"+username+"'")
			if(status=='COMPILATION ERROR'):
				cursor.execute("update score set score=score-25 where username='"+username+"'")
				cursor.execute("update score set time=time+"+str(time)+" where username='"+username+"'")
				
			db.commit()
		    except:
			db.rollback()
		    f.close()
	    elif(choice=='2'):
		    db1 = MySQLdb.connect("localhost","root","","minor",3306,"/opt/lampp/var/mysql/mysql.sock" )
		    cursor1 = db1.cursor()
		    cursor1.execute("SELECT * FROM score order by score desc, time")
		    results = cursor1.fetchall()
		    scoreboard=''
		    scoreboard=scoreboard+'Username\tScore\tTime\n'
		    for row in results:
			    scoreboard=scoreboard+str(row[0])+'\t'+str(row[1])+'\t'+str(row[2])+'\n'
		    db1.close()
		    conn.send(scoreboard)	    
		    conn.recv(1)
	    elif(choice=='3'):
		    db1 = MySQLdb.connect("localhost","root","","minor",3306,"/opt/lampp/var/mysql/mysql.sock" )
		    cursor1 = db1.cursor()
		    cursor1.execute("SELECT id,question,language,result,time FROM submission where username='"+username+"'")
		    results = cursor1.fetchall()
		    prevruns=''
		    if(cursor1.rowcount > 0):
			    for row in results:
				    prevruns=prevruns+'ID:'+str(row[0])+'\nQuestion:'+str(row[1])+'\nLanguage:'+str(row[2])+'\nResult:'+str(row[3])+'\nTime:'+str(row[4])+'\n\n'
		    else:
		            prevruns='NO PREVIOUS RUNS'
			
		    db1.close()
		    conn.send(prevruns)	  
		    conn.recv(1)
	    elif(choice=='4'):
		    time1=datetime.datetime.now().replace(microsecond=0)
		    conn.send('Time left is '+str(endtime-time1))
		    conn.recv(1)
    try:
	cursor.execute("update loggedin set status='NO' where username='"+username+"'")
	cursor.execute("update loggedin set ip='NULL' where username='"+username+"'")
	db.commit()
    except:
	db.rollback()
    db.close()
    print "user "+username+" exited"
    conn.close()



class App:
	
    def __init__(self, master):
	frame = Frame(master, width=2000, height=1000,bg="#000000",  colormap="new")
	#image1 = tk.PhotoImage(file="jii.gif")
	#w = image1.width()
	#h = image1.height()
	#backgroundImage=image1
	#root.geometry("%dx%d+0+0" % (w, h))
	#panel1 = tk.Label(root, image=image1)
	#panel1.pack(side='top', fill='both', expand='yes')
	frame.pack()
	master.title("LOGIN SCREEN")
	#photo=PhotoImage(file="jii.gif")
        #backgroundImage=photo
	
	
	#img = PIL.Image.open("jii.gif")
	#backgroundImage=ImageTk.PhotoImage(img)
	abc=tkFont.Font(family="Helvetica", size=40, weight ='bold' )	
	abc1=tkFont.Font(family="Helvetica", size=16, weight='bold' )
	abc2=tkFont.Font(family="Helvetica", size=20, weight='bold' )
	abc3=tkFont.Font(family="Helvetica", size=15, weight='bold' )

	#l.place(relx=0.45, rely=0.15, anchor=CENTER)
	#l=Labe#l(frame, text="CODE  SAGE", font=abc, bg="#ffa700")
        #l.pack()
	#l.place(relx=0.45, rely=0.15, anchor=CENTER)
	l=Label(frame, text="CODE SAGE", font=abc, bg="black", fg="#ffa700")	
	l.pack()
	
	l=Label(frame, text="coding round", font=abc3,bg="black", fg="#ffa700")
        l.pack()
        l.place(relx=0.45, rely=0.2, anchor=CENTER)
	l1=Label(frame, text="Username:", font=abc2, bg="black", fg="#ffa700")
	l1.pack()
	l1.place(relx=0.2, rely=0.57, anchor=CENTER)
        l2=Label(frame, text="Password:", bg="black", fg="#ffa700", font=abc2)
	l2.pack()
	l2.place(relx=0.2, rely=0.67, anchor=CENTER)

        self.e1 = Entry(frame, font=abc2, fg="#ffa700")
	self.e1.pack(side=RIGHT,padx=15, pady=15)
	self.e1.place(relx=0.6, rely=0.57, anchor=CENTER)
        self.e2 = Entry(frame,show="*", font=abc2)
	self.e2.place(relx=0.6, rely=0.67, anchor=CENTER)

	#photo=PhotoImage(file="jii.gif")
	#ph=Label(frame,image=photo, bg="#ffa700")
	#ph.photo=photo
	#ph.pack()
	#ph.place(relx=0.03,rely=0.03)
	        
	button1 = self.button = Button(frame, text="LOGIN",font=abc1, command=self.login)
        button1.pack(side=LEFT,padx=10, pady=50)
	button1.configure(width = 10,background="#ffa700", activebackground = "#ff4f03" ,activeforeground="lightyellow",highlightcolor="#ff4f03",)
	button1.place(relx=0.33, rely=0.83, anchor=CENTER)		
	button2=self.button = Button(frame,compound=TOP, text="QUIT", font=abc1, command=frame.quit)
	button2.pack(side=LEFT)
	button2.configure(width = 10,background="#ffa700", activebackground = "#ff4f03" ,activeforeground="lightyellow",highlightcolor="#ff4f03",)
	button2.place(relx=.67, rely=0.83, anchor=CENTER)			

	frame.propagate(False)		
    def login(self):
	global s	
	username=self.e1.get()	
	password=self.e2.get()	
	sql = "SELECT * FROM login"
	flag=0
	s=socket.socket()
	try:
	   cursor.execute(sql)
	   results = cursor.fetchall()
	   for row in results:
		if( row[0]==username and row[1]==password and row[2]=='admin' ):
			flag=1
	except:
	   tkMessageBox.showinfo("ERROR", "Error: unable to fetch data")	
	   sys.exit(0)
	if(flag==0):
	   tkMessageBox.showinfo("ERROR", "Wrong Credentials. Exiting...")	
	   sys.exit(0)
	root.destroy()
	global root1	
	root1=Tk()	
	app = App1(root1)

def checktime(s):
    global endtime
    while True:
	time.sleep(1)
	time1=datetime.datetime.now().replace(microsecond=0)
	if(time1>endtime):
		print 'Contest ends'	
		break
def showscore():
	db1 = MySQLdb.connect("localhost","root","","minor",3306,"/opt/lampp/var/mysql/mysql.sock" )
	cursor1 = db1.cursor()
	cursor1.execute("SELECT * FROM score order by score desc, time")
	results = cursor1.fetchall()
	print 'Username,Score,Time'
	for row in results:
		print row[0],',',row[1],',',row[2]
	db1.close()

class App1:
	
    def __init__(self, master):
	master.title("LOGIN SCREEN1")
	frame = Frame(master, width=2000, height=1000, bg="black",  colormap="new")
	frame.pack()
	abc=tkFont.Font(family="Helvetica", size=40, weight ='bold' )	
	abc1=tkFont.Font(family="Helvetica", size=13, weight ='bold' )
	abc2=tkFont.Font(family="Helvetica", size=20, weight ='bold' )
	abc3=tkFont.Font(family="Helvetica", size=15, weight ='bold' )

	l=Label(frame, text="CODE SAGE", font=abc, bg="black",fg="#ffa700")
	#l.place(relx=0.45, rely=0.1, anchor=CENTER)
 	l.pack()
 	l=Label(frame, text="coding round", font=abc3,bg="black", fg="#ffa700")
        l.pack()
        l.place(relx=0.45, rely=0.2, anchor=CENTER)
	#l=Label(frame, text="SAGE", font=abc, bg="#ffa700")	
	#l.pack()
	
	

	#photo=PhotoImage(file="jii.gif")
	#ph=Label(frame,image=photo , bg="black")
	#ph.photo=photo
	#ph.pack()
	#ph.place(relx=0.03,rely=0.03)
	button1 = self.button = Button(frame, text="  ADD  QUESTIONS  ",font=abc1, command=self.addquestions)
        button1.pack(side=LEFT,padx=15, pady=55)
	button1.configure(width = 20,background="#ffa700", activebackground = "#ff4f03" ,activeforeground="lightyellow",highlightcolor="#ff4f03",)
	button1.place(relx=0.45, rely=0.3, anchor=CENTER)		
	button1 = self.button = Button(frame, text="       ADD USERS      ",font=abc1, command=self.addusers)
        button1.pack(side=LEFT,padx=15, pady=55)
	button1.configure(width = 20,background="#ffa700", activebackground = "#ff4f03" ,activeforeground="lightyellow",highlightcolor="#ff4f03",)
	button1.place(relx=0.45, rely=0.5, anchor=CENTER)
	button2=self.button = Button(frame, text=" SET CONTEST TIME", font=abc1, command=self.contest)
	button2.pack(side=LEFT,padx=15, pady=55)
	button2.configure(width = 20,background="#ffa700", activebackground = "#ff4f03" ,activeforeground="lightyellow",highlightcolor="#ff4f03",)
	button2.place(relx=0.45, rely=0.7, anchor=CENTER)		
	button1 = self.button = Button(frame, text="  START  CONTEST  ",font=abc1, command=self.login)
        button1.pack(side=LEFT,padx=15, pady=55)
	button1.configure(width = 20,background="#ffa700", activebackground = "#ff4f03" ,activeforeground="lightyellow",highlightcolor="#ff4f03",)
	button1.place(relx=0.45, rely=0.9, anchor=CENTER)				
	button1 = self.button = Button(frame, text="            EXIT            ",font=abc1, command=frame.quit)
        button1.pack(side=LEFT,padx=15, pady=55)
	button1.configure(width = 20,background="#ffa700", activebackground = "#ff4f03" ,activeforeground="lightyellow",highlightcolor="#ff4f03",)
	button1.place(relx=0.85, rely=0.1, anchor=CENTER)	
	frame.propagate(False)		

    def login(self):
	conteststart()
	#os.system('python chat/pyChat.py')  #s
	thread.start_new_thread(checktime,(s,))
        tkMessageBox.showinfo("Message", "Server starts.")
	root1.destroy()
	'''global root2	
	root2=Tk()	
	app = App2(root2)'''
    def addquestions(self):
	global questionsflag
	questionsflag=1
	f=open("questions.csv","r")
	ques=f.readlines()
	for que in ques:
		try:
			cursor.execute("insert into questions values('"+que.strip()+"')")
			db.commit()
		except:
			db.rollback()
	f.close()
        tkMessageBox.showinfo("Message", "Questions added.")

    def addusers(self):
	global usersflag
	usersflag=1
	db1 = MySQLdb.connect("localhost","root","","minor",3306,"/opt/lampp/var/mysql/mysql.sock" )
	cursor1 = db1.cursor()
	f=open("users.csv","r")
	users=f.readlines()
	for user in users:
		try:	
			use=user.strip().split('\t')
			cursor1.execute("insert into login values('"+use[0]+"','"+use[1]+"','user')")
			db1.commit()
		except:
			db1.rollback()
	cursor1.execute("SELECT * FROM login where priv='user'")
	results = cursor1.fetchall()
	try:
		for row in results:
			cursor1.execute("insert into loggedin(username,status) values('"+row[0]+"','NO')")
			cursor1.execute("insert into score values('"+row[0]+"',0,0)")
			db1.commit()
	except:
		db1.rollback()
	db1.close()
	f.close()
        tkMessageBox.showinfo("Message", "Users added.")
    def contest(self):
	global contesttimesec,contesttimesetflag
	inp=tkSimpleDialog.askstring('String', 'Enter contest time?')
	a=re.compile("[0-9]+:[0-9]+:[0-9]+")
	if(bool(a.match(inp)) == True):
		contesttime=inp.split(':')
		contesttimesec=int(contesttime[0])*3600+int(contesttime[1])*60+int(contesttime[2])
		contesttimesetflag=1
	else:
	        tkMessageBox.showinfo("INVALID TIME", "FORMAT SHOULD BE LIKE 'HH:MM:SS'")



db = MySQLdb.connect("localhost","root","","minor",3306,"/opt/lampp/var/mysql/mysql.sock" )
cursor = db.cursor()
subid=0
contestflag=0
usersflag=0
questionsflag=0
contesttimesetflag=0
contesttimesec=0
cursor.execute("delete from loggedin")
cursor.execute("delete from login where priv='user'")
cursor.execute("delete from questions")
cursor.execute("delete from score")
cursor.execute("delete from accepted")
cursor.execute("delete from submission")
db.commit()
starttime=datetime.datetime.now().replace(microsecond=0)
endtime=datetime.datetime.now().replace(microsecond=0)

root = Tk()
app = App(root)
root.mainloop()
print "\n\n-----------------------LOG-----------------------\n\n"
while True:
	conn,addr=s.accept()
	thread.start_new_thread(handleclient,(conn,addr,))
	time1=datetime.datetime.now().replace(microsecond=0)
        if(time1>endtime):
		break

