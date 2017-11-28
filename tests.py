from unittest import TestCase
from models import Loan
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
