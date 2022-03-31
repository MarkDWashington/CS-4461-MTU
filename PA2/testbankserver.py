import unittest

import bankserver


class TestBankServer(unittest.TestCase):
    def testTransactionParseSequenceNum(self):
        t = bankserver.Transaction("000000001BAL00512300000000123")
        self.assertEqual(t.sequenceNum, 1)

    def testTransactionParseType(self):
        t = bankserver.Transaction("000000001BAL00512300000000123")
        self.assertEqual(t.type, "BAL")

    def testTransactionParseDigits(self):
        t = bankserver.Transaction("000000001BAL00512300000000123")
        self.assertEqual(t.digits, 5)

    def testTransactionParseAmount(self):
        t = bankserver.Transaction("000000001BAL00512300000000123")
        self.assertEqual(t.amount, 123.00)

    def testTransactionParseChecksum(self):
        t = bankserver.Transaction("000000001BAL00512300000012400")
        self.assertEqual(t.checksum, 12400)
