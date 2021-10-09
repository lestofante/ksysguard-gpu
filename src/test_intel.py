import unittest

import threading, intel

class TestIntelParser(unittest.TestCase):
    def test_txt(self):
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
        

if __name__ == '__main__':
    unittest.main()
