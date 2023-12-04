class Nvidia:
    def __init__(self, allGpu, mutex):
        self.allGpu = allGpu
        self.mutex = mutex
        self.header = ['index', 'temperature', 'utilization.%', 'memory.%', 'fan.speed', 'pstate', 'power.draw.w', 'clocks.sm.mhz', 'clocks.memory.mhz', 'clocks.graphics.mhz']

    def getCommand(self):
        return ["nvidia-smi", "--query-gpu=index,temperature.gpu,utilization.gpu,utilization.memory,fan.speed,pstate,power.draw,clocks.sm,clocks.mem,clocks.gr", "--format=csv", '--loop=1']

    def parseLine(self, line):
        line = str(line)
        
        if len(line) < 5:
            return
        
        line = line[2:-3]
        
        parameters = [s for s in line.split(',') if s]

        # Fixes possible nvidia-smi cmd errors # 29
        if len(parameters) == 0:
            return

        if not parameters[0].isdigit():
            # this should be the header
            return
        
        if len(parameters) != len(self.header):
            print( "Nvidia parse line error: I am expecting "+len(self.header)+" parameter but I got " + len(parameters) )
            return
        
        gpuName = "Nvidia." + parameters[0]
        
        with self.mutex:
            for index, parameter in enumerate(parameters):
                value = [s for s in parameter.split(' ') if s]
                self.allGpu[gpuName+"."+self.header[index]] = value[0]
