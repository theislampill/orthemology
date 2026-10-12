import unittest
from contract_check import analyse

class SourceRecordContractTest(unittest.TestCase):
    def test_exact_operation_relative_alphabets(self):
        result = analyse()
        self.assertEqual(result.get('minimum_alphabets'), {'content_only': 1, 'content_and_voice': 2, 'content_voice_and_work_exclusion': 3})

if __name__ == '__main__':
    unittest.main()
