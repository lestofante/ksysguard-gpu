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
                self.header += ['fReq', 'fAct']
            
            if p == 'IRQ':
                self.header += ['irq.second']
            
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
        parameters = parameters[:-1]           # Remove trailing '\n'
        if parameters[0] == "b'":
            parameters = parameters[1:]        # Remove preceding b'
        if len(parameters[0]) == 6:            # Frequency is a 4-digit number, preceded by b'
            parameters[0] = parameters[0][2:]  # Remove preceding b' leaving only the integer
        
        if not parameters[0].isdigit():
            if len(self.header) == 0:
                self.extrapolate(parameters)
                # print("Intel parse extrapolated header list: " + str(self.header))
            return

        if len(parameters) != len(self.header):
            print("Intel parse line error: I am expecting " + str(len(self.header)) + " parameters but I got "
                  + str(len(parameters)) + "! Parsed line is\n" + line )
            return
        
        gpuName = "Intel.0"
        with self.mutex:
            for index, parameter in enumerate(parameters):
                self.allGpu[gpuName+"."+self.header[index]] = parameter
