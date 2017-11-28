from unittest import TestCase
from models import Loan, LoanException1, LoanException2
from missioncap_parser import parse_into_loan
from datetime import date

# Tests go here.
class ParseIntoLoanTest(TestCase):
    def test(self):
        csv_loan = self.get_csv_loan()
        loan = parse_into_loan(csv_loan)
        self.assertTrue(isinstance(loan, Loan))

        # Test that only a subset of fields were imported correctly, as we do
        # not need all of them.
        self.assertEqual(9742242.06, loan.id)
        self.assertEqual(date(2386, 11, 20), loan.maturity_date)
        self.assertEqual(date(2349, 5, 31), loan.completion_date)
        self.assertEqual(9.8, loan.current_ltv)
        self.assertEqual(8.46, loan.original_ltv)
        self.assertEqual(39727.77, loan.cms)
        self.assertEqual(69.7, loan.current_interest_rate)
        self.assertEqual(71618.01, loan.borrower_income_1)
        self.assertEqual(7926468.41, loan.borrower_income_2)
        self.assertEqual('L', loan.fitch_product_category)

    def get_csv_loan(self):
        return {
            'Arrears Balance': '5505032.35',
            'Bankruptcy Marker': 'N',
            'CMS': '39727.77',
            'Completion Date': '23490531',
            'Current Index': 'FIX',
            'Current Interest Rate': '69.7',
            'Current LTV': '9.8',
            'Current Margin': '0.53',
            'CurrentBalance': '97209880.57',
            'DataExtract Date': '198705',
            'Fitch Product Category': 'L',
            'FTB Flag': 'N',
            'Further Advance': 'Y',
            'Income Borrower 1': '71618.01',
            'Income Borrower 2': '7926468.41',
            'Index Reference Rate': '7.35',
            'Interest Rate Type': 'fixed',
            'Latest Valuation Amount': '148848212.62',
            'Latest Valuation Date': '19840209',
            'Loan ID': '9742242.06',
            'Loan Purpose': 'OT',
            'Maturity Date': '23861120',
            'Months in Arrears': '44744.91',
            'No of CCJs': '1.13',
            'Occupancy': 'POW',
            'Original Balance': '89709174.08',
            'Original LTV': '8.46',
            'Original Term': '33.98',
            'Originator Product Category': 'Biggest Yacht',
            'Originator': 'SPML',
            'Portfolio': '3780858.82',
            'Possession Flag': 'Somewhat possessive',
            'Property ID': '5441940.3',
            'Property Type': 'BU',
            'Region': 'UK',
            'Repayment Type': 'PP',
            'Reversion Date': '19870525',
            'Reversionary Index': 'OTH',
            'Reversionary Margin': '0.48',
            'RTB Flag': 'N',
            'Self Cert Flag': 'Y',
            'Tenure': 'Feudal',
            'Value of CCJs': '25539.92',
        }


class LoanException1Test(TestCase):
    def setUp(self):
        self.loan_exception = LoanException1()

    def test_broken_by_loan(self):
        loan = Loan()
        loan.maturity_date = date(2017, 1, 1)
        loan.completion_date = date(2017, 1, 2)

        self.assertTrue(self.loan_exception.broken_by_loan(loan))

    def test_broken_by_loan_completion_before_maturity(self):
        loan = Loan()
        loan.maturity_date = date(2017, 1, 2)
        loan.completion_date = date(2017, 1, 1)

        self.assertFalse(self.loan_exception.broken_by_loan(loan))

    def test_broken_by_loan_completion_equal_maturity(self):
        loan = Loan()
        loan.maturity_date = date(2017, 1, 1)
        loan.completion_date = date(2017, 1, 1)

        self.assertFalse(self.loan_exception.broken_by_loan(loan))

    def test_get_loan_penalty(self):
        loan = Loan()
        self.assertEqual(4, self.loan_exception.get_loan_penalty(loan))




class LoanException2Test(TestCase):
    def setUp(self):
        self.loan_exception = LoanException2()

    def test_broken_by_loan(self):
        loan = Loan()
        loan.current_index = 'FIX'
        loan.current_margin = 5
        loan.current_interest_rate = 3

        self.assertTrue(self.loan_exception.broken_by_loan(loan))

    def test_broken_by_loan_index_mismatch(self):
        loan = Loan()
        loan.current_index = ''
        loan.current_margin = 5
        loan.current_interest_rate = 5

        self.assertFalse(self.loan_exception.broken_by_loan(loan))

    def test_broken_by_loan_margin_match(self):
        loan = Loan()
        loan.current_index = 'FIX'
        loan.current_margin = 5
        loan.current_interest_rate = 5

        self.assertFalse(self.loan_exception.broken_by_loan(loan))

    def test_get_loan_penalty(self):
        testcases = [
            ('U', 1),
            ('P', 1),
            ('N', 1),
            ('L', 2),
            ('M', 2),
            ('B', 3),
        ]
        for category, penalty in testcases:
            with self.subTest(category=category):
                loan = Loan()
                loan.fitch_product_category = category
                self.assertEqual(
                    penalty,
                    self.loan_exception.get_loan_penalty(loan)
                )
