import unittest

from exchagerate_api import Exchagerate_APIConn_Daily

class TestExchagerateAPI(unittest.TestCase):
    def test_transform_raw_data(self):
        try:
            api_obj = Exchagerate_APIConn_Daily('2021-01-01')
        except Exception as e:
            # If an exception is raised, fail the test.
            self.fail('Failed to connect to API: {}'.format(e))