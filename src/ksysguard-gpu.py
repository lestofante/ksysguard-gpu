#!/usr/bin/env python3

import subprocess
import traceback
import intel, amd, nvidia
####################################################

class Runner:
    def __init__(self, parser, clientConnectedEvent):
        self.runnerAlive = True
        self.p = None
        self.parser = parser
        self.clientConnectedEvent = clientConnectedEvent
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        

    def isAlive(self):
        return self.thread.is_alive()

    def close(self):
        self.runnerAlive = False
        if self.p is not None:
            try:
                self.p.kill()
            except:
                traceback.print_exc()

    def run(self):
        exe = self.parser.getCommand()
        while (self.runnerAlive):
            self.clientConnectedEvent.wait()
            try:
                self.p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                print(exe[0] + ': found and running')
                while self.p.poll() is None and self.clientConnectedEvent.is_set():
                    line = self.p.stdout.readline()
                    try:
                        self.parser.parseLine(line)
                    except:
                        print(exe[0] + ': exception while parsing the line, please report the bug ' + str(line))
                        traceback.print_exc()
                self.p.kill()
                time.sleep(1)
            except FileNotFoundError:
                print(exe[0] + ': executable not found')
                # stop this runner
                self.runnerAlive = False
            except:
                traceback.print_exc()
                print(exe[0] + ': process has died! Maybe need root')
            
            print(exe[0] + ': process stopped')
            time.sleep(1)
        
        print(exe[0] + ': terminated')

def parseCommand(line, mutex):
    line=line.strip()
    answer = ""
    with mutex:
        try:
            if line == 'monitors':
                for key in allGpu.keys():
                    answer += key+'\tinteger\n'
            elif line[-1:] == '?':
                answer += (line[:-1]+'\t0\t100\n')
            else:
                answerValue = allGpu.get(line, -1)
                answer += (str(answerValue)+'\n')
        except:
            #ignore all exception
            pass

    answer += 'ksysguardd> '
    return answer

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

parserIntel = intel.Intel(allGpu, mutex)
parserAmd = amd.Amd(allGpu, mutex)
parserNvidia = nvidia.Nvidia(allGpu, mutex)

clientConnectedEvent = threading.Event()

clientConnectedEvent.set()

t1 = Runner(parserIntel, clientConnectedEvent)
t2 = Runner(parserAmd, clientConnectedEvent)
t3 = Runner(parserNvidia, clientConnectedEvent)

# we need to sincronize access to 'allGpu'
gpuFount = 0
while len(allGpu) == 0 and (t1.isAlive() or t2.isAlive() or t3.isAlive()):
    with mutex:
        gpuFount = len(allGpu)
    time.sleep(0.5)

clientConnectedEvent.clear()

if not t1.isAlive() and not t2.isAlive() and not t3.isAlive():
    print("No data source is alive")
    exit (-1)

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(0)

try:
    # Bind the socket to the port
    server_address = ('localhost', 3112)
    print ('starting up on %s port %s' % server_address)
    server.bind(server_address)

    # Listen for incoming connections
    server.listen(5) 

    # Sockets from which we expect to read
    inputs = [ server ]

    message_queues = {}


    while inputs:
        #if at least one client is connected
        if len(inputs) > 1:
            clientConnectedEvent.set()
        else:
            clientConnectedEvent.clear()
        
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
                        answer = parseCommand(lines[i], mutex)
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
    print("closing server")
    server.close()
    t1.close()
    t2.close()
    t3.close()
