#testProcessData.py
#Alicia Melotik
#amelotik@nd.edu
#Marco Tchernychev
#mtcherny@nd.edu

import unittest
from processdata import calcStat, filter, fetch

data = "http://ns-mn1.cse.nd.edu/cse20289-fa24/hw03/data-all.json"

class TestClass(unittest.TestCase):
    def test_count(self): 
        self.assertEqual(calcStat(filter(fetch(data), '2024-*-*', '03', 'iface=eth0;dir=downlink;type=iperf' ), 'count' ), )
    def test_mean(self): 
        self.assertEqual(calcStat(filter(fetch(data), '2024-03-*', '*', 'iface=eth0;dir=uplink;type=iperf' ), 'mean' ), )
    def test_median(self): 
        self.assertEqual(calcStat(filter(fetch(data), '2024-06-*', '*', 'iface=eth0;dir=uplink;type=iperf' ), 'median' ), )
    def test_min(self): 
        self.assertEqual(calcStat(filter(fetch(data), '2024-*-*', '20', 'iface=wlan0;dir=uplink;type=iperf' ), 'min' ), )
    def test_max(self): 
        self.assertEqual(calcStat(filter(fetch(data), '2024-07-*', '17', 'iface=wlan0;dir=downlink;type=iperf' ),  'max' ), )
    def test_stddev(self): 
        self.assertEqual(calcStat(filter(fetch(data), '2024-*-*', '*' ), 'stddev' ), )

if __name__ == "__main__":
    unittest.main()