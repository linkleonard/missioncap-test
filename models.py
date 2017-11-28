
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


class LoanException2(LoanException):
    def broken_by_loan(self, loan):
        return (
            loan.current_index == 'FIX' and
            loan.current_margin != loan.current_interest_rate
        )

    def get_loan_penalty(self, loan):
        # Assume that loan always has a valid category
        penalty_by_category = {
            'U': 1,
            'P': 1,
            'N': 1,
            'L': 2,
            'M': 2,
            'B': 3,
        }
        return penalty_by_category[loan.fitch_product_category]


class LoanException3(LoanException):
    def broken_by_loan(self, loan):
        return loan.current_ltv > loan.original_ltv

    def get_loan_penalty(self, loan):
        # Assume that loan always has a valid category
        penalty_by_category = {
            'U': 0,
            'P': 2,
            'N': 4,
            'L': 6,
            'M': 8,
            'B': 10,
        }
        return penalty_by_category[loan.fitch_product_category]


class LoanException4(LoanException):

    def broken_by_loan(self, loan):
        return loan.cms > self._get_monthly_income(loan)

    def get_loan_penalty(self, loan):
        # Assume that CMS is non-zero

        # Penalty values for each category correspond to the percentage
        # difference between the CMS and the maximum monthly payment a debtor
        # can pay. The indices for each category correspond to the following
        # values:
        # 0: 0-10%
        # 1: 10.01-20%
        # 2: 20.01-30%
        # 3: 30.01-50%
        # 4: 50.01-100%
        loan_penalty_map = {
            "U": [0, 0, 1, 3, 10],
            "P": [2, 3, 5, 12, 20],
            "N": [4, 6, 9, 20, 40],
            "L": [6, 10, 14, 30, 50],
            "M": [8, 13, 21, 40, 60],
            "B": [10, 20, 30, 50, 80],
        }

        category_penalties = loan_penalty_map[loan.fitch_product_category]

        monthly_income = self._get_monthly_income(loan)
        difference_percentage = (loan.cms - monthly_income) / loan.cms * 100
        penalty_index = self._get_penalty_index(difference_percentage)

        return category_penalties[penalty_index]

    def _get_monthly_income(self, loan):
        total_income = loan.borrower_income_1 + loan.borrower_income_2
        return total_income / 12

    def _get_penalty_index(self, percentage):
        penalty_maximums = (10, 20, 30, 50, 100)
        for index, maximum in enumerate(penalty_maximums):
            if percentage <= maximum:
                return index
