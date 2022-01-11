class Amd:
    def __init__(self, allGpu, mutex):
        self.allGpu = allGpu
        self.mutex = mutex

    def getCommand(self):
        return ["radeontop", "-d-"]

    def parseLine(self, line):
        line=str(line)
        
        if len(line) < 5:
            return
        
        #remove b''
        line = line[2:-3]
        
        line = line.strip()
        line = line.split(':', 1) # remove timestamp
        if len(line) != 2:
            return
        line = line[1]
        
        parameters = line.split(',')
        gpuName = None
        with self.mutex:
            for parameter in parameters:
                keyValue = parameter.split(' ')
                
                if len(keyValue) < 3:
                    continue
                
                if keyValue[1] == "bus":
                    gpuName = 'AMD.'+keyValue[2]
                    self.allGpu[gpuName+"."+keyValue[1]] = keyValue[2]

                if gpuName is not None:
                    for val in keyValue:
                        if val[-1:] == "%":
                            self.allGpu[gpuName+"."+keyValue[1]+'.%'] = val[:-1] #remove . and %
                        elif val[-2:] == "mb":
                            self.allGpu[gpuName+"."+keyValue[1]+'.mb'] = val[:-2] #remove . and mb
                        elif val[-3:] == "ghz":
                            self.allGpu[gpuName+"."+keyValue[1]+'.ghz'] = val[:-3] #remove . and mb
