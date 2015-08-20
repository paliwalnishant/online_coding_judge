import socket,time,thread
import sys
import getpass,os
import datetime
host=''
port=50017
s=socket.socket()
try:
	s.connect((host,port))
except:
	print 'Server down'
	sys.exit(0)


print 'ENTER USERNAME:'
username=raw_input()
s.send(username)
s.recv(1)
print 'ENTER PASSWORD:'
password=getpass.getpass()
s.send(password)
s.recv(1)
x=s.recv(30)
if(x!="0"):
	print x
	sys.exit(0) 
endtime=s.recv(20)
s.send('0')
while True:
    	print ('1.Submit\n2.Check Scoreboard\n3.View Previous runs\n4.Check time\n5.Exit')
	choice=raw_input()	
	s.send(choice)	
	time1=datetime.datetime.now().replace(microsecond=0)
	endtime1=datetime.datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S")	
	if(time1>endtime1):
		print 'Contest ends'	
		choice='5'
	if(choice=='1'):

		queslist=s.recv(1024)
		s.send('0')
		print queslist

		print 'ENTER Question NAME:'
		quesname=raw_input()

		s.send(quesname)
		x=s.recv(1)
		if x!='0':
			print "Question not found"
			sys.exit(0)

		print 'Enter the extension of the file:'
		fileext=raw_input()
		while(True):
			print 'Enter the name of the file:'
			filename=raw_input()
			if(os.path.isfile(filename)==True):
				break
			print 'File Not Found'
		s.send(fileext)
		x=s.recv(1)
		s.send(filename)
		x=s.recv(1)
		f=open (filename, "rb") 
		data=f.read()
		f.close()
		s.send(str(len(data)))
		s.recv(1)
		s.send(data)
		print s.recv(1024)
		s.send('0')
	elif(choice=='2'):
		print s.recv(1024)
		s.send('1')
	elif(choice=='3'):
		print s.recv(1024)
		s.send('1')
	elif(choice=='4'):
		print s.recv(1024)
		s.send('1')
	elif(choice=='5'):
		break
s.close()
