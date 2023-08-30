import calendar
from datetime import datetime, timedelta

class BudgetService:
    @staticmethod
    def query(start, end):
        if start > end:
            return 0

        budget_list = BudgetRepo.get_all()

        for day in BudgetRepo.get_every_day():
            day_budget = 0




    @staticmethod
    def _get_days_in_month(year, month) -> int:
        return calendar.monthrange(year, month)[1]

    @staticmethod
    def _get_duration_month(start, end):
        return []  # YYYYmm, YYYYmm

    @staticmethod
    def get_per_day_budget(year, month, amount) -> int:
        return amount / BudgetService._get_days_in_month(year, month)

    @staticmethod
    def get_every_day(start, end):
        day_list = [start.day]
        while start.day <= end.day:
            start.day += timedelta(days=1)
            day_list.append()
        return day_list

class BudgetRepo:
    @staticmethod
    def get_all():
        pass


class Budget:
    def __init__(self, year_month, amount) -> None:
        self.year_month = year_month
        self.amount = amount
