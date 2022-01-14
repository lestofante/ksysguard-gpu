#!/usr/bin/env python3

import subprocess
import traceback

import select
import socket
import sys
import threading
import time

import intel
import amd
import nvidia


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

def parseCommand(line, mutex, allGpu):
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
        except e:
            print("error: "+str(e))
            # Ignore all exceptions
            pass

    answer += 'ksysguardd> '
    return answer


####################################################
#                      MAIN                        #
####################################################

def main():
    allGpu = {}
    mutex = threading.Lock()

    parserIntel = intel.Intel(allGpu, mutex)
    parserAmd = amd.Amd(allGpu, mutex)
    parserNvidia = nvidia.Nvidia(allGpu, mutex)

    clientConnectedEvent = threading.Event()

    clientConnectedEvent.set()

    t_INTEL = Runner(parserIntel, clientConnectedEvent)
    t_AMD = Runner(parserAmd, clientConnectedEvent)
    t_NVIDIA = Runner(parserNvidia, clientConnectedEvent)

    # Synchronize access to 'allGpu'
    print("Waiting for a data source to produce valid data")
    nbGpuFound = 0
    while len(allGpu) == 0 and (t_INTEL.isAlive() or t_AMD.isAlive() or t_NVIDIA.isAlive()):
        with mutex:
            nbGpuFound = len(allGpu)
        time.sleep(0.5)

    print("Got valid data, proceeding")

    clientConnectedEvent.clear()

    if not t_INTEL.isAlive() and not t_AMD.isAlive() and not t_NVIDIA.isAlive():
        print("No data source is alive")
        exit (-1)

    # Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setblocking(0)

    try:
        # Bind the socket to the port
        server_address = ('127.0.0.1', 9876)
        print('Starting up on %s port %s' % server_address)
        server.bind(server_address)

        # Listen for incoming connections
        server.listen(5) 

        # Sockets from which we expect to read
        inputs = [server]

        message_queues = {}


        while inputs:
            # If at least one client is connected
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
                    print('New connection from', client_address)
                    connection.setblocking(0)
                    inputs.append(connection)
                    message_queues[connection] = ""
                    
                    connection.send(b"ksysguardd 1.2.0\nksysguardd> ")
                else:
                    # A "readable" client socket has sent us some data
                    data = s.recv(1024)
                    if data:
                        data = data.decode("utf-8", "strict")
                        message_queues[s] += data
                        lines = message_queues[s].split('\n')
                        linesNumber = len(lines)
                        for i in range(0, linesNumber-1):
                            answer = parseCommand(lines[i], mutex, allGpu)
                            s.send(answer.encode('utf-8'))
                        message_queues[s] = lines[linesNumber-1]
                    else:
                        # Interpret empty result as closed connection
                        print('Client disconnected: ', client_address)
                        # Stop listening for input on the connection
                        inputs.remove(s)
                        s.close()
                        # Remove message queue
                        del message_queues[s]
    finally:
        print("Closing server")
        server.close()
        t_INTEL.close()
        t_AMD.close()
        t_NVIDIA.close()

if __name__ == '__main__':
    main()
