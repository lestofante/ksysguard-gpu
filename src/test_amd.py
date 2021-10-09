import unittest

import threading, amd

class TestAmdParser(unittest.TestCase):
    def test_txt(self):
        allGpu = {}
        mutex = threading.Lock()
        parser = amd.Amd(allGpu, mutex)
        with open('../test_files/radeontop_output.txt', 'r') as file1:
            for line in file1.readlines():
                parser.parseLine(line)
        #1633822330.719917: bus 09, gpu 0.00%, ee 0.00%, vgt 0.00%, ta 0.00%, sx 0.00%, sh 0.00%, spi 0.00%, sc 0.00%, pa 0.00%, db 0.00%, cb 0.00%, vram 16.15% 1311.39mb, gtt 0.97% 78.85mb, mclk 100.00% 0.875ghz, sclk 1.11% 0.023ghz

        expected = {}
        expected['AMD.09.bus'] = '09'
        expected['AMD.09.cb.%'] = '0.00'
        expected['AMD.09.db.%'] = '0.00'
        expected['AMD.09.ee.%'] = '0.00'
        expected['AMD.09.gpu.%'] = '0.00'
        expected['AMD.09.gtt.%'] = '0.97'
        expected['AMD.09.gtt.mb'] = '78.85'
        expected['AMD.09.mclk.%'] = '100.00'
        expected['AMD.09.mclk.ghz'] = '0.875'
        expected['AMD.09.pa.%'] = '0.00'
        expected['AMD.09.sc.%'] = '0.00'
        expected['AMD.09.sclk.%'] = '1.11'
        expected['AMD.09.sclk.ghz'] = '0.023'
        expected['AMD.09.sh.%'] = '0.00'
        expected['AMD.09.spi.%'] = '0.00'
        expected['AMD.09.sx.%'] = '0.00'
        expected['AMD.09.ta.%'] = '0.00'
        expected['AMD.09.vgt.%'] = '0.00'
        expected['AMD.09.vram.%'] = '16.15'
        expected['AMD.09.vram.mb'] = '1311.39'
        
        self.assertEqual(expected, allGpu)
        

if __name__ == '__main__':
    unittest.main()
