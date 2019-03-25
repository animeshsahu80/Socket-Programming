import socket
import os
import sys
import random
import datetime
import hashlib


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print "Socket created"
port=12345
port_udp = 12347


def ret_date_time(date,time):
	date1 = tuple(map(int,date.split('-')))
	time1 = tuple(map(int,time.split(':')))
	return date1,time1

def ret_time(f):
	ft=datetime.datetime.fromtimestamp(os.path.getmtime(f))
	return ft
def shortlist(c,date1,time1,date2,time2):
	
	date11 ,time11 =ret_date_time(date1,time1)
	date22 ,time22 =ret_date_time(date2,time2)
	strtime = datetime.datetime(date11[0],date11[1],date11[2],time11[0],time11[1],time11[2])
	endtime = datetime.datetime(date22[0],date22[1],date22[2],time22[0],time22[1],time22[2])
	arr=[]
	files = filter(os.path.isfile, os.listdir( os.curdir ) )
	l=len(files)
	if l==0:
		ans = "No such files in current directory"
		c.send(ans.encode())
		print ans
	else:
		for f in files:
			ftime = ret_time(f)
			name, ext = os.path.splitext(f)
			if ftime>strtime and ftime<endtime:
				ans = "name: " + f + "   size: " + str(os.path.getsize(f)) + "   timestamp: " + ftime.strftime('%Y-%m-%d %H:%M:%S') + "   extension: " + ext
				c.send(ans.encode())
				print ans
	rem = '||end||';
	c.send(rem.encode())
	if len(files)!=0:
		print 'Sent detail successfully'

def shortlist_spc(c,date1,time1,date2,time2,type1):
	date11 ,time11 =ret_date_time(date1,time1)
	date22 ,time22 =ret_date_time(date2,time2)
	strtime = datetime.datetime(date11[0],date11[1],date11[2],time11[0],time11[1],time11[2])
	endtime = datetime.datetime(date22[0],date22[1],date22[2],time22[0],time22[1],time22[2])
	files = filter(os.path.isfile, os.listdir( os.curdir ) )
	n = 0
	flag=0
	type1 = type1[1:5]
	l=len(files)
	for f in files:
		ftime = ret_time(f)
		name, ext = os.path.splitext(f)
		if ftime>strtime and ftime<endtime and ext==type1:
			ans = "name: " + f + "   size: " + str(os.path.getsize(f)) + "   timestamp: " + ftime.strftime('%Y-%m-%d %H:%M:%S') + "   extension: " + ext
			c.send(ans.encode())
			print ans
			n = n+1
	if n!=0:
		print 'Sent detail successfully'
	else:
		ans = "No such files of given format in current directory"
		c.send(ans.encode())
		print ans
	rem = "||end||"
	c.send(rem.encode())



def longlist(c):
	files = filter(os.path.isfile, os.listdir( os.curdir ) )
	l=len(files)
	flag=0
	if len(files)==0:
		ans = "No files in current directory"
		c.send(ans.encode())
		print ans
	else:
		for f in files:
			ftime = ret_time(f)
			name, ext = os.path.splitext(f)
			ans = "name of the file: " + f + "   size: " + str(os.path.getsize(f)) + "   timestamp: " + ftime.strftime('%Y-%m-%d %H:%M:%S') + "   extension: " + ext
			c.send(ans.encode())
			print ans
	rem = '||end||';
	l=len(files)
	c.send(rem.encode())
	if len(files)!=0:
		print 'Sent detail successfully'

def longlist_specific(c):
	files = filter(os.path.isfile, os.listdir( os.curdir ) )
	n = 0;
	count=0
	for f in files:
		count=count+1
		ftime = datetime.datetime.fromtimestamp(os.path.getmtime(f))
		name, ext = os.path.splitext(f)
		flag = 0
		if ext == '.txt':
			term = "programmer"
			file = open(f)
			for line in file:
				count=count+1
				line = line.strip().split(' ')
				if term in line:
					#
					flag = 1
					break;
			file.close()
		if flag==1:
			ans = "name: " + f + "   size: " + str(os.path.getsize(f)) + "   timestamp: " + ftime.strftime('%Y-%m-%d %H:%M:%S') + "   extension: " + ext
			c.send(ans.encode())
			print ans
			n = n+1
	if n!=0:
		print 'Sent detail successfully'
	else:
		ans = "No text files containing word programmer"
		c.send(ans.encode())
		print ans
	rem = '||end||';
	c.send(rem.encode())

def Filehashsingle(c,file):
	hash_md5 = hashlib.md5()
	flag=0
	try:
		with open(file, "rb") as f:
			count=0
			for chunk in iter(lambda: f.read(4096), b""):
				hash_md5.update(chunk)
				count=count+1
		ans = "hash: " + hash_md5.hexdigest()+ "   timestamp: " + datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
		c.send(ans.encode())
		print 'Sent detail successfully'
	except:
		print 'File does not exist'
		c.send(ans.encode())

def Filehashmultiple(c):
	files = filter(os.path.isfile, os.listdir( os.curdir ) )
	for file in files:
		hash_md5 = hashlib.md5()
		flag=0
		with open(file, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hash_md5.update(chunk)
		ans = "name: "+file +"   hash: " + hash_md5.hexdigest() + "   timestamp: " + datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
		c.send(ans.encode())
	rem = '||end||'
	c.send(rem.encode())
	print 'Sent detail successfully'

def sendFile(c,file):
	try:
		f = open(file,'rb')
	except:
		print('error opening file')
	l = f.read(1024)
	while (l):
		c.send(l)
		l = f.read(1024)
	print 'file sent success fully'
	f.close()
	arr=[]
	flag=0
	hash_md5 = hashlib.md5()
	with open(file, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	ans = "name of the file: " + file + "   size: " + str(os.path.getsize(file)) + "   timestamp: " + datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S') + "   hash: " + hash_md5.hexdigest()
	c.send(ans.encode())

def sendFile_udp(c,file,port_udp,host):
	udp_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	dest = (host, port_udp)
	try:
		f=open(file,'rb')
	except:
		print('error opening file')
	l=f.read(1024)
	fr=[]
	while(l):
		if(udp_soc.sendto(l,dest)):
			l = f.read(1024)
	udp_soc.close()
	f.close()
	hash_md5 = hashlib.md5()
	soc=[]
	with open(file, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	ans = "name: " + file + "   size: " + str(os.path.getsize(file)) + "   timestamp: " + datetime.datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S') + "   hash: " + hash_md5.hexdigest()
	c.send(ans.encode())


host = socket.gethostname()
s.bind((host, port))
s.listen(5)
sct=[]
while True:
	try:
		c,addr=s.accept()
		s.settimeout(.5)
		count=0
		print("Connection from: " + str(addr))

		while True:
			val=c.recv(1024).decode()
			
			valid = val.strip().split(' ')
			l=len(valid)
			if len(valid)>=6 and valid[1]=='shortlist':
				if len(valid)==6:
					shortlist(c,valid[2],valid[3],valid[4],valid[5])
				elif len(valid)==7:
					shortlist_spc(c,valid[2],valid[3],valid[4],valid[5],valid[6])
			elif len(valid)>=2 and valid[1]=='longlist':
				if len(valid)==2:
					longlist(c)
				elif len(valid)==3:
					longlist_specific(c)
			elif len(valid)>=2 and valid[0]=='FileHash':
				if len(valid)==3 and valid[1]=='verify':
					Filehashsingle(c,valid[2])
				elif len(valid)==2 and valid[1]=='checkall':
					Filehashmultiple(c)
			elif len(valid)==4 and valid[0] == 'FileDownload':
				if valid[3]=='TCP':
					sendFile(c,valid[1])
				elif valid[3]=='UDP':
					sendFile_udp(c,valid[1],port_udp,host)
			else:
				print 'Invalid Command'
				break
	except KeyboardInterrupt:
		print 'Socket Closed'
		s.close()
		sys.exit()
	except socket.timeout:
		print 'Client Disconnected'
		s.settimeout(None)
	c.close()
s.close()