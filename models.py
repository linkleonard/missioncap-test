
class Loan(object):
    def __init__(self):
        raise NotImplemented()


class LoanException(object):
    def __init__(self, id=None):
        self.id = id

    def broken_by_loan(self, loan):
        raise NotImplemented()

    def get_loan_penalty(self, loan):
        raise NotImplemented()

    def __str__(self):
        return 'LoanException {id}'.format(id=self.id)


loan_exceptions = []
