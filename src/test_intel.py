import unittest

import threading, intel

class TestIntelParser(unittest.TestCase):
    def test_txt1(self):
        allGpu = {}
        mutex = threading.Lock()
        parser = intel.Intel(allGpu, mutex)
        with open('../test_files/intel_gpu_output.txt', 'r') as file1:
            for line in file1.readlines():
                parser.parseLine(line)
            
        expected = {}
        expected['Intel.0.fReq'] = '5'
        expected['Intel.0.fAtt'] = '5'
        expected['Intel.0.irq/s'] = '11'
        expected['Intel.0.rc6.%'] = '97'
        expected['Intel.0.gpu'] = '0.06'
        expected['Intel.0.pkg'] = '8.23'
        expected['Intel.0.RCS.%'] = '2.00'
        expected['Intel.0.RCS.se'] = '3'
        expected['Intel.0.RCS.wa'] = '4'
        expected['Intel.0.BCS.%'] = '5.00'
        expected['Intel.0.BCS.se'] = '6'
        expected['Intel.0.BCS.wa'] = '7'
        expected['Intel.0.VCS.%'] = '8.00'
        expected['Intel.0.VCS.se'] = '9'
        expected['Intel.0.VCS.wa'] = '0'
        expected['Intel.0.VECS.%'] = '1.00'
        expected['Intel.0.VECS.se'] = '2'
        expected['Intel.0.VECS.wa'] = '3'
        
        self.assertEqual(expected, allGpu)
        
    def test_txt2(self):
        self.maxDiff = None
        allGpu = {}
        mutex = threading.Lock()
        parser = intel.Intel(allGpu, mutex)
        with open('../test_files/intel_gpu_output_2.txt', 'r') as file1:
            for line in file1.readlines():
                parser.parseLine(line)
            
        expected = {}
        expected['Intel.0.fReq'] = '223'
        expected['Intel.0.fAtt'] = '223'
        expected['Intel.0.irq/s'] = '412'
        expected['Intel.0.rc6.%'] = '48'
        expected['Intel.0.gpu'] = '0.43'
        expected['Intel.0.pkg'] = '3.98'
        expected['Intel.0.rd'] = '2526'
        expected['Intel.0.wr'] = '1076'
        expected['Intel.0.RCS.%'] = '43.06'
        expected['Intel.0.RCS.se'] = '0'
        expected['Intel.0.RCS.wa'] = '0'
        expected['Intel.0.BCS.%'] = '0.00'
        expected['Intel.0.BCS.se'] = '0'
        expected['Intel.0.BCS.wa'] = '0'
        expected['Intel.0.VCS.%'] = '0.00'
        expected['Intel.0.VCS.se'] = '0'
        expected['Intel.0.VCS.wa'] = '0'
        expected['Intel.0.VECS.%'] = '0.00'
        expected['Intel.0.VECS.se'] = '0'
        expected['Intel.0.VECS.wa'] = '0'
        
        self.assertEqual(expected, allGpu)
        
    def test_txt3(self):
        self.maxDiff = None
        allGpu = {}
        mutex = threading.Lock()
        parser = intel.Intel(allGpu, mutex)
        with open('../test_files/intel_gpu_output_3.txt', 'r') as file1:
            for line in file1.readlines():
                parser.parseLine(line)
            
        expected = {}
        expected['Intel.0.fReq'] = '217'
        expected['Intel.0.fAtt'] = '217'
        expected['Intel.0.irq/s'] = '590'
        expected['Intel.0.rc6.%'] = '51'
        expected['Intel.0.gpu'] = '0.34'
        expected['Intel.0.pkg'] = '5.34'
        expected['Intel.0.rd'] = '4881'
        expected['Intel.0.wr'] = '1905'
        expected['Intel.0.RCS.%'] = '28.76'
        expected['Intel.0.RCS.se'] = '0'
        expected['Intel.0.RCS.wa'] = '0'
        expected['Intel.0.BCS.%'] = '0.00'
        expected['Intel.0.BCS.se'] = '0'
        expected['Intel.0.BCS.wa'] = '0'
        expected['Intel.0.VCS.%'] = '0.00'
        expected['Intel.0.VCS.se'] = '0'
        expected['Intel.0.VCS.wa'] = '0'
        expected['Intel.0.VECS.%'] = '0.00'
        expected['Intel.0.VECS.se'] = '0'
        expected['Intel.0.VECS.wa'] = '0'
        
        self.assertEqual(expected, allGpu)
        

if __name__ == '__main__':
    unittest.main()
