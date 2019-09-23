#!/bin/python3

import select
import socket
import sys
import threading
import subprocess
import time

allGpu = dict()
mutex = threading.Lock()

def parseLineIntel(line):
	global allGpu, mutex
	line=str(line)
	line = line[2:-3]
	
	parameters = [s for s in line.split(' ') if s]
	
	if not parameters[0].isdigit():
		#print('ignored: ', parameters[0])
		return
	
	indexNames = ['fReq', 'fAtt', 'irq/s', 'rc6%', 'Watt', 'rcs%', 'rcsSe', 'rcsWa', 'bcs%', 'bcsSe', 'bcsWa', 'vcs%', 'vcsSe', 'vcsWa', 'vecs%', 'vecsSe', 'vecsWa']
	if len(parameters) != len(indexNames):
		return
	
	gpuName = "Intel"
	mutex.acquire()
	try:
		for index, parameter in enumerate(parameters):
			allGpu[gpuName+"."+indexNames[index]] = parameter
			#print('intel got ', indexNames[index], ' as ', parameter)
	finally:
		mutex.release()


def runInteltop():
	exe = ["intel_gpu_top", "-l"]
	
	p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	while p.poll() is None:
		line = p.stdout.readline()
		parseLineIntel(line)
	print('intel_gpu_top process has died! probably is not installed, or need root')

def parseLine(line):
	global allGpu, mutex
	line=str(line)
	
	line = line[18:-1] #remove timestamp and \n
	parameters = line.split(',')
	gpuName = None
	mutex.acquire()
	try:
		for parameter in parameters:
			keyValue = parameter.split(' ')
			
			if len(keyValue) < 3:
				continue
			
			if keyValue[1] == "bus":
				gpuName = 'bus'+keyValue[2]
				allGpu[gpuName+"."+keyValue[1]] = keyValue[2]

			if keyValue[2][-1:] == "%":
				allGpu[gpuName+"."+keyValue[1]] = keyValue[2][:-4] #remove . and %
	finally:
		mutex.release()


def runRadeontop():
	exe = ["radeontop", "-t120", "-d-"]
	p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	while p.poll() is None:
		line = p.stdout.readline()
		parseLine(line)
	print('radeontop process has died! probably is not installed, or need root')

t = threading.Thread(target=runRadeontop)
t.start()

t = threading.Thread(target=runInteltop)
t.start()

#just mutex lol
mutex.acquire()
while len(allGpu) == 0:
	mutex.release()
	time.sleep(0.5)
	mutex.acquire()
mutex.release()

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(0)

# Bind the socket to the port
server_address = ('localhost', 3112)
print ('starting up on %s port %s' % server_address)
server.bind(server_address)

# Listen for incoming connections
server.listen(5) 

# Sockets from which we expect to read
inputs = [ server ]

message_queues = {}


def parseCommand(line):
	line=line.strip()
	answer = ""
	mutex.acquire()
	try:
		if line == 'monitors':
			for key in allGpu.keys():
				answer += key+'\tinteger\n'
		elif line[-1:] == '?':
			answer += (line[:-1]+'\t0\t100\n')
		else:
			answerValue = allGpu.get(line)
			if answerValue is None:
				answerValue = 0
			answer += (str(answerValue)+'\n')
	except:
		pass
	finally:
		mutex.release()

	print ('request "%s" answer %s' % (line, answer))
	answer += 'ksysguardd> '
	return answer

try:
	while inputs:
		# Wait for at least one of the sockets to be ready for processing
		readable, writable, exceptional = select.select(inputs, [], [])
		
		# Handle inputs
		for s in readable:
			if s is server:
				# A "readable" server socket is ready to accept a connection
				connection, client_address = s.accept()
				print ('new connection from', client_address)
				connection.setblocking(0)
				inputs.append(connection)
				message_queues[connection] = ""
				
				connection.send(b"ksysguardd 1.2.0\nksysguardd> ")
			else:
				# A "readable" cliet socket has sent us some data
				data = s.recv(1024)
				if data:
					data = data.decode("utf-8", "strict")
					print ('received "%s" from %s' % (data, s.getpeername()))
					message_queues[s] += data
					lines = message_queues[s].split('\n')
					linesNumber = len(lines)
					for i in range(0, linesNumber-1):
						answer = parseCommand(lines[i])
						s.send(answer.encode('utf-8'))
					message_queues[s] = lines[linesNumber-1]
				else:
					# Interpret empty result as closed connection
					print ('closing', client_address, 'after reading no data')
					# Stop listening for input on the connection
					inputs.remove(s)
					s.close()
					# Remove message queue
					del message_queues[s]
finally:
	server.close()
	print("server closed")
