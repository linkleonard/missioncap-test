
class Loan(object):
    def __init__(self):
        self.id = None
        self.maturity_date = None
        self.completion_date = None
        self.current_index = ''
        self.current_margin = 0
        self.current_ltv = 0
        self.original_ltv = 0
        self.cms = 0
        self.current_interest_rate = 0
        self.borrower_income_1 = 0
        self.borrower_income_2 = 0
        self.fitch_product_category = ''


class LoanException(object):
    def __init__(self, id=None):
        self.id = id

    def broken_by_loan(self, loan):
        raise NotImplemented()

    def get_loan_penalty(self, loan):
        raise NotImplemented()

    def __str__(self):
        return 'LoanException {id}'.format(id=self.id)


class LoanException1(LoanException):
    def broken_by_loan(self, loan):
        return loan.maturity_date < loan.completion_date

    def get_loan_penalty(self, loan):
        return 4


loan_exceptions = [
    LoanException1(id=1),
]
