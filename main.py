from csv import DictReader, DictWriter
from models import (
    LoanException1,
    LoanException2,
    LoanException3,
    LoanException4,
)
from missioncap_parser import parse_into_loan
from argparse import ArgumentParser


LOAN_ID_FIELD = 'Loan ID'
LOAN_GRADE_FIELD = 'Loan Grade'
LOAN_EXCEPTIONS_FIELD = 'Exception IDs'
INITIAL_LOAN_GRADE = 100

def get_exceptions_for_loans(loans, loan_exceptions):
    for loan in loans:
        exceptions = [
            loan_exception
            for loan_exception in loan_exceptions
            if loan_exception.broken_by_loan(loan)
        ]
        yield (loan, exceptions)


def get_loan_report_rows(loans_with_exceptions):
    for loan, broken_exceptions in loans_with_exceptions:
        # Convert iterable into a tuple so we can iterate over it multiple
        # times, in case it is a simple generator.
        exceptions = tuple(broken_exceptions)
        grade_penalties = (
            loan_exception.get_loan_penalty(loan)
            for loan_exception in exceptions
        )
        loan_grade = INITIAL_LOAN_GRADE - sum(grade_penalties)

        sorted_exception_ids = sorted(loan_exception.id for loan_exception in exceptions)
        yield {
            LOAN_ID_FIELD: loan.id,
            LOAN_GRADE_FIELD: loan_grade,
            LOAN_EXCEPTIONS_FIELD: '|'.join(str(exception_id) for exception_id in sorted_exception_ids)
        }


def main():
    # TODO: load this file name from CLI arguments
    parser = get_argument_parser()
    args = parser.parse_args()

    output_filename = args.output
    loan_database_filename = args.loan_database

    output_file_fields = (LOAN_ID_FIELD, LOAN_GRADE_FIELD, LOAN_EXCEPTIONS_FIELD)

    loan_exceptions = [
        LoanException1(id=1),
        LoanException2(id=2),
        LoanException3(id=3),
        LoanException4(id=4),
    ]

    with open(output_filename, 'w') as output_file:
        with open(loan_database_filename, 'r') as loan_file:
            reader = DictReader(loan_file)
            writer = DictWriter(output_file, fieldnames=output_file_fields)

            parsed_loans = (parse_into_loan(row) for row in reader)
            loans_with_exceptions = get_exceptions_for_loans(parsed_loans, loan_exceptions)
            writer.writerows(get_loan_report_rows(loans_with_exceptions))


def get_argument_parser():
    parser = ArgumentParser()
    parser.add_argument('loan_database')
    parser.add_argument('output')
    return parser


if __name__ == '__main__':
    main()
