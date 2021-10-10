class Intel:
    def __init__(self, allGpu, mutex):
        self.allGpu = allGpu
        self.mutex = mutex
        self.header = []
        
    def getCommand(self):
        return ["intel_gpu_top", "-l"]

    def extrapolate(self, parameters):
        for p in parameters:
            if p == 'Freq':
                self.header += ['fReq', 'fAtt']
            
            if p == 'IRQ':
                self.header += ['irq/s']
            
            if p == 'RC6':
                self.header += ['rc6.%']
            
            if p == 'Power':
                self.header += ['gpu', 'pkg']
            
            if p == 'IMC':
                self.header += ['rd', 'wr']
            
            possibleDivider = p.find('/')
            
            if possibleDivider != -1:
                if p[possibleDivider+1:].isdigit():
                    name = p[:possibleDivider]# + '.' + p[possibleDivider+1:]
                    self.header += [name+'.%', name+'.se', name+'.wa']

    def parseLine(self, line):
        line=str(line)
        
        if len(line) < 5:
            return
        
        line = line.strip()
        
        parameters = [s for s in line.split(' ') if s]
        
        if not parameters[0].isdigit():
            if len(self.header) == 0:
                self.extrapolate(parameters)
                #print("Intel parse extrapolated header list: " + str(self.header))
            return

        if len(parameters) != len(self.header):
            print( "Intel parse line error: I am expecting " + str(len(self.header)) + " parameter but I got " + str(len(parameters)) + " parsed line is " + line )
            return
        
        gpuName = "Intel.0"
        with self.mutex:
            for index, parameter in enumerate(parameters):
                self.allGpu[gpuName+"."+self.header[index]] = parameter
