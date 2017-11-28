# parser is a built-in module. Let's just use a different name.
from datetime import date
from models import Loan


def noop(value):
    return value


def parse_date(value):
    year = int(value[0:4])
    month = int(value[4:6])
    day = int(value[6:8])

    return date(year, month, day)


loan_csv_mapping = [
    {
        'fieldname': 'id',
        'source_field': 'Loan ID',
        'parser': float,
    },
    {
        'fieldname': 'maturity_date',
        'source_field': 'Maturity Date',
        'parser': parse_date,
    },
    {
        'fieldname': 'completion_date',
        'source_field': 'Completion Date',
        'parser': parse_date,
    },
    {
        'fieldname': 'current_index',
        'source_field': 'Current Index',
        'parser': noop,
    },
    {
        'fieldname': 'current_margin',
        'source_field': 'Current Margin',
        'parser': float,
    },
    {
        'fieldname': 'current_ltv',
        'source_field': 'Current LTV',
        'parser': float,
    },
    {
        'fieldname': 'original_ltv',
        'source_field': 'Original LTV',
        'parser': float,
    },
    {
        'fieldname': 'cms',
        'source_field': 'CMS',
        'parser': float,
    },
    {
        'fieldname': 'current_interest_rate',
        'source_field': 'Current Interest Rate',
        'parser': float,
    },
    {
        'fieldname': 'borrower_income_1',
        'source_field': 'Income Borrower 1',
        'parser': float,
    },
    {
        'fieldname': 'borrower_income_2',
        'source_field': 'Income Borrower 2',
        'parser': float,
    },
]


def parse_into_loan(row):
    loan = Loan()
    for field in loan_csv_mapping:
        fieldname = field['fieldname']
        parser = field['parser']
        value = row[field['source_field']]
        setattr(loan, fieldname, parser(value))

    return loan
