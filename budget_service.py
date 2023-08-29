import calendar
from datetime import datetime

class BudgetService:
    @staticmethod
    def query(start, end):
        if start > end:
            return 0

        budget_list = BudgetRepo.get_all()

        start_month_days = BudgetService._get_days_in_month(start.year, start.month)

        result = 0
        for budget in budget_list:
            budget_year = int(budget.year_month[:4])
            budget_month = int(budget.year_month[4:])
            budget_start = datetime(budget_year, budget_month, 1)
            last_day = calendar.monthrange(budget_year, budget_month)[1]
            budget_end = datetime(budget_year, budget_month, last_day)
            if budget_start <= start <= budget_end and budget_start <= end <= budget_end:
                duration = end - start
                result += (duration.days + 1) * BudgetService.get_per_day_budget(budget_year, budget_month, budget.amount)
            elif start <= budget_start and end >= budget_end:
                result += budget.amount
            elif budget_start <= start <= budget_end:
                duration = start_month_days - start.day
                result += (duration + 1) * BudgetService.get_per_day_budget(budget_year, budget_month, budget.amount)
            elif budget_start <= end <= budget_end:
                result += end.day * BudgetService.get_per_day_budget(budget_year, budget_month, budget.amount)
        return result

    @staticmethod
    def _get_days_in_month(year, month) -> int:
        return calendar.monthrange(year, month)[1]

    @staticmethod
    def _get_duration_month(start, end):
        return []  # YYYYmm, YYYYmm

    @staticmethod
    def get_per_day_budget(year, month, amount) -> int:
        return amount / BudgetService._get_days_in_month(year, month)

class BudgetRepo:
    @staticmethod
    def get_all():
        pass


class Budget:
    def __init__(self, year_month, amount) -> None:
        self.year_month = year_month
        self.amount = amount
