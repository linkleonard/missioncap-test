from csv import DictReader, DictWriter
from .models import Loan, loan_exceptions

LOAN_ID_FIELD = 'Loan ID'
LOAN_GRADE_FIELD = 'Loan Grade'
LOAN_EXCEPTIONS_FIELD = 'Exception IDs'


def parse_into_loan(row):
    raise NotImplemented()


def get_exceptions_for_loans(loans):
    for loan in loans:
        exceptions = [
            loan_exception
            for loan_exception in load_exceptions
            if load_exception.broken_by_loan(loan)
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

        yield {
            LOAN_ID_FIELD: loan.id,
            LOAN_GRADE_FIELD: load_grade,
            LOAN_EXCEPTIONS_FIELD: '|'.join(loan_exception in exceptions)
        }


def main():
    # TODO: load this file name from CLI arguments
    filename = 'loan_data.csv'
    output_file_fields = (LOAN_ID_FIELD, LOAN_GRADE_FIELD, LOAN_EXCEPTIONS_FIELD)

    with open(output_filename, 'w') as output_file:
        with open(filename, 'r') as loan_file:
            reader = DictReader(loan_file)
            writer = DictWriter(output_file, fieldnames=output_file_fields)

            parsed_loans = (parse_into_loan(row) for row in reader)
            loans_with_exceptions = get_exceptions_for_loans(parsed_loans)
            writer.writerows(get_loan_report_rows(loans_with_exceptions))


if __name__ == '__main__':
    main()
