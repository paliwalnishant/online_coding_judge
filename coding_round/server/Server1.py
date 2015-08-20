import socket,thread
import sys
import MySQLdb
import getpass
import os
import filecmp
import commands
import datetime
import time
def conteststart():
	global starttime,contestflag,endtime,contesttimesec
	contestflag=1
	host='172.16.82.190'
	port=50017
	s.bind((host,port))
	s.listen(5)
	starttime=datetime.datetime.now().replace(microsecond=0)
	endtime=starttime + datetime.timedelta(seconds=contesttimesec)
	print 'Contest starts at: ',starttime,' and will end at:',endtime
	

def handleclient(conn,addr):
    global subid,starttime
    db = MySQLdb.connect("localhost","root","root","pcj" )
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
    choice=conn.recv(1)
    time1=datetime.datetime.now().replace(microsecond=0)
    if(time1>endtime):
	    choice='5'
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
			cursor.execute("insert into accepted values('"+username+"','"+quesname+"','"+str(subtime)+"')")
			cursor.execute("update score set score=score+1 where username='"+username+"'")
			cursor.execute("update score set time=time+"+str(time)+" where username='"+username+"'")
		db.commit()
	    except:
		db.rollback()
	    f.close()
    elif(choice=='2'):
	    db1 = MySQLdb.connect("localhost","root","root","pcj" )
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
	    db1 = MySQLdb.connect("localhost","root","root","pcj" )
	    cursor1 = db1.cursor()
	    cursor1.execute("SELECT id,question,language,result,time FROM submission where username='"+username+"'")
	    results = cursor1.fetchall()
	    prevruns=''
	    for row in results:
		    prevruns=prevruns+'ID:'+str(row[0])+'\nQuestion:'+str(row[1])+'\nLanguage:'+str(row[2])+'\nResult:'+str(row[3])+'\nTime:'+str(row[4])+'\n\n'
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

def clienthandler(s):
    while True:
    	conn,addr=s.accept()
    	thread.start_new_thread(handleclient,(conn,addr,))

def checktime(s):
    global endtime
    while True:
	time.sleep(1)
	time1=datetime.datetime.now().replace(microsecond=0)
	if(time1>endtime):
		print 'Contest ends'	
		break
def showscore():
	db1 = MySQLdb.connect("localhost","root","root","pcj" )
	cursor1 = db1.cursor()
	cursor1.execute("SELECT * FROM score order by score desc, time")
	results = cursor1.fetchall()
	print 'Username,Score,Time'
	for row in results:
		print row[0],',',row[1],',',row[2]
	db1.close()

	
db = MySQLdb.connect("localhost","root","root","pcj" )
cursor = db.cursor()
subid=0
contestflag=0
usersflag=0
questionsflag=0
contesttimesetflag=0
contesttimesec=0
print 'ENTER ADMIN USERNAME:'
username=raw_input()
print 'ENTER ADMIN PASSWORD:'
password=getpass.getpass()
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
   print "Error: unable to fetch data"
   sys.exit(0)
if(flag==0):
   print "Wrong Credentials. Exiting..."
   sys.exit(0)

cursor.execute("delete from loggedin")
cursor.execute("delete from login where priv='user'")
cursor.execute("delete from questions")
cursor.execute("delete from score")
cursor.execute("delete from accepted")
cursor.execute("delete from submission")
db.commit()
starttime=datetime.datetime.now().replace(microsecond=0)
endtime=datetime.datetime.now().replace(microsecond=0)
while True:
    if(contestflag==0):
    	print ('1.START CONTEST\n2.ADD QUESTIONS\n3.ADD USERS\n4.SET CONTEST TIME\n5.EXIT')
    else:
    	print ('1.SHOW TIME\n2.UPDATE QUESTIONS\n3.UPDATE USERS\n4.SHOW SCOREBOARD\n5.EXIT')
    choice=raw_input()
    time1=datetime.datetime.now().replace(microsecond=0)
    if(time1>endtime and contestflag==1):
	showscore()	
	choice='6'	
    if(choice=='1' and contestflag==0):
	if(usersflag==0):
		print 'Please add users first'
		continue
	if(questionsflag==0):
		print 'Please add questions first'
		continue
	if(contesttimesetflag==0):
		print 'Please set contest time first'
		continue
	conteststart()
	thread.start_new_thread(clienthandler,(s,))
	thread.start_new_thread(checktime,(s,))
    elif(choice=='1' and contestflag==1):
        time1=datetime.datetime.now().replace(microsecond=0)
        print('Time left is '+str(endtime-time1))
    elif(choice=='2'):
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
    elif(choice=='3'):
	usersflag=1
	db1 = MySQLdb.connect("localhost","root","root","pcj" )
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
    elif(choice=='4' and contestflag==0):
	print 'Enter contest time:'
	contesttime=raw_input().split(':')
	contesttimesec=int(contesttime[0])*3600+int(contesttime[1])*60+int(contesttime[2])
	contesttimesetflag=1
    elif(choice=='5'):
	break
    elif(choice=='4' and contestflag==1):
	showscore()
s.close()
db.close()
