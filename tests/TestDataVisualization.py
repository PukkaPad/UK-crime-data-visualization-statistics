import unittest
from bin import DataVisualization

class TestDataVisualization(unittest.TestCase):
    def Test_loaddata_ok(self):
        result = DataVisualization.loadData('../data/')
        self.assertEquals("<class 'pandas.core.frame.DataFrame'>", str(type(result)))

    def Test_loaddata_nopath(self):
        result = DataVisualization.loadData()
        self.assertEquals("<class 'pandas.core.frame.DataFrame'>", str(type(result)))

