#!/bin/python3

import subprocess

####################################################

class Intel:
	def __init__(self, allGpu, mutex):
		self.allGpu = allGpu
		self.mutex = mutex
	
	def parseLine(self, line):
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
		self.mutex.acquire()
		try:
			for index, parameter in enumerate(parameters):
				self.allGpu[gpuName+"."+indexNames[index]] = parameter
				#print('intel got ', indexNames[index], ' as ', parameter)
		finally:
			self.mutex.release()


	def run(self):
		exe = ["intel_gpu_top", "-l"]
		try:
			p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			while p.poll() is None:
				line = p.stdout.readline()
				self.parseLine(line)
		except:
			print('intel_gpu_top process has died! probably is not installed, or need root')

####################################################

class Amd:
	def __init__(self, allGpu, mutex):
		self.allGpu = allGpu
		self.mutex = mutex

	def parseLine(self, line):
		line=str(line)
		
		line = line[18:-1] #remove timestamp and \n
		parameters = line.split(',')
		gpuName = None
		self.mutex.acquire()
		try:
			for parameter in parameters:
				keyValue = parameter.split(' ')
				
				if len(keyValue) < 3:
					continue
				
				if keyValue[1] == "bus":
					gpuName = 'bus'+keyValue[2]
					self.allGpu[gpuName+"."+keyValue[1]] = keyValue[2]

				if keyValue[2][-1:] == "%":
					self.allGpu[gpuName+"."+keyValue[1]] = keyValue[2][:-4] #remove . and %
		finally:
			self.mutex.release()


	def run(self):
		exe = ["radeontop", "-t120", "-d-"]
		try:
			p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			while p.poll() is None:
				line = p.stdout.readline()
				self.parseLine(line)
		except:
			print('radeontop process has died! probably is not installed, or need root')


####################################################

class Nvidia:
	def __init__(self, allGpu, mutex):
		self.allGpu = allGpu
		self.mutex = mutex

	def run(self):
		print('nvidia-smi is not currently supported')

####################################################
#                      MAIN                        #
####################################################
import select
import socket
import sys
import threading
import time

allGpu = {}
mutex = threading.Lock()

parserIntel = Intel(allGpu, mutex)
parserAmd = Amd(allGpu, mutex)
parserNvidia = Nvidia(allGpu, mutex)

t = threading.Thread(target=parserAmd.run)
t.start()

t = threading.Thread(target=parserIntel.run)
t.start()

t = threading.Thread(target=parserNvidia.run)
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
					message_queues[s] += data
					lines = message_queues[s].split('\n')
					linesNumber = len(lines)
					for i in range(0, linesNumber-1):
						answer = parseCommand(lines[i])
						s.send(answer.encode('utf-8'))
					message_queues[s] = lines[linesNumber-1]
				else:
					# Interpret empty result as closed connection
					print ('client disconnected: ', client_address)
					# Stop listening for input on the connection
					inputs.remove(s)
					s.close()
					# Remove message queue
					del message_queues[s]
finally:
	server.close()
	print("server closed")

