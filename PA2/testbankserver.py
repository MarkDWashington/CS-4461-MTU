import unittest

import bankserver


class TestBankServer(unittest.TestCase):
    def test_Transaction_ParseSequenceNum(self):
        t = bankserver.Transaction("000000001DEP00512300000012301")
        self.assertEqual(t._sequenceNum, 1)

    def test_Transaction_ParseType(self):
        t = bankserver.Transaction("000000001DEP00512300000012301")
        self.assertEqual(t._type, "DEP")

    def test_Transaction_ParseDigits(self):
        t = bankserver.Transaction("000000001DEP00512300000012301")
        self.assertEqual(t._digits, 5)

    def test_Transaction_ParseAmount(self):
        t = bankserver.Transaction("000000001DEP00512300000012301")
        self.assertEqual(t._amount, 123.00)

    def test_Transaction_ParseChecksum(self):
        t = bankserver.Transaction("000000001DEP005123000000012301")
        self.assertEqual(t._checksum, 12301)

    def test_Transaction_ParseBALSeqNum(self):
        t = bankserver.Transaction("000000000BAL000000000000000")
        self.assertEqual(t._sequenceNum, 0)
    
    def test_Transaction_ParseBALType(self):
        t = bankserver.Transaction("000000000BAL000000000000000")
        self.assertEqual(t._type, "BAL")
    
    def test_Transaction_ParseBALDigits(self):
        t = bankserver.Transaction("000000000BAL000000000000000")
        self.assertEqual(t._digits, 0)

    def test_Transaction_ParseBALAmount(self):
        t = bankserver.Transaction("000000000BAL000000000000000")
        self.assertEqual(t._amount, 0)
    
    def test_Transaction_ParseBALChecksum(self):
        t = bankserver.Transaction("000000000BAL000000000000000")
        self.assertEqual(t._checksum, 0)

    def test_Transaction_IncorrectBALSeqNum(self):
        t = bankserver.Transaction("000000000BAL000000000000000")
        self.assertRaises(bankserver.MalformedPacketException)