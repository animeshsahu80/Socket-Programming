import socket
import sys
import os
import datetime
import hashlib
import random

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print "Socket created"


def shortlist(socket1):
	while 1:
		data = socket1.recv(1024).decode()
		l=len(data)
		if data.endswith('||end||'):
			print data[:-7]
			break
		print data

def longlist(socket1):
	while 1:
		data = socket1.recv(1024).decode()
		l=len(data)
		if data.endswith('||end||'):
			print data[:-7]
			break
		print data

def Filehashsingle(socket1):
	data = socket1.recv(1024).decode()
	l=len(data)
	print data

def Filehashmultiple(socket1):
	while 1:
		data = socket1.recv(1024).decode()
		l=len(data)
		if data.endswith('||end||'):
			print data[:-7]
			break
		print data

def downloadFile(s,file1,message):
	with open(file1, 'wb') as f:
		s.send(message.encode())
		while 1:
			data = s.recv(1024)
			l=len(data)
			f.write(data)
			if len(data) < 1024:
				break
	print 'File downloaded'
	f.close()
	data = s.recv(1024).decode()
	print data

def downloadFile_udp(s,file1,host,port_udp,message):
	udp_soc=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp_soc.bind((host, port_udp))
	f = open(file1, 'wb')
	s.send(message.encode())
	data, addr = udp_soc.recvfrom(1024)
	try:
		while(data):
			f.write(data)
			udp_soc.settimeout(2)
			data, addr=udp_soc.recvfrom(1024)
	except socket.timeout:
		f.close()
		udp_soc.close()
	data = s.recv(1024).decode()
	print data
	print 'File Downloaded'


port_udp = 12347
port=12345
host=socket.gethostname()
s.connect((host, port))

while True:
	try:
		message = raw_input("command-> ")

		while True:
			msg = message.strip().split(' ')
			if msg[0] == 'Exit' or msg[0]=='exit':
				print 'Socket Closed'
				s.close()
				sys.exit()
			elif msg[1]=='shortlist':
				s.send(message.encode())
				shortlist(s)
			elif msg[1]=='longlist':
				s.send(message.encode())
				longlist(s)
			elif msg[0]=='FileHash':
				s.send(message.encode())
				if msg[1]=='verify':
					Filehashsingle(s)
				else:
					Filehashmultiple(s)
			elif msg[0] == 'FileDownload':
				if msg[3]=='TCP':
					downloadFile(s,msg[2],message)
				else:
					downloadFile_udp(s,msg[2],host,port_udp,message)
			else:
				print 'Invalid Command'
			message = raw_input("command-> ")
	except KeyboardInterrupt:
		print 'Socket Closed'
		s.close()
		sys.exit()
	
