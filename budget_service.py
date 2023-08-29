import calendar
from datetime import datetime


class BudgetService:
    @staticmethod
    def query(start: datetime, end: datetime) -> float:
        """

        :param start: datetime, ex. datetime(2023, 7, 15)
        :param end: datetime, ex. datetime(2023, 7, 16)
        :return: float, ex. 100.0
        """
        # early return if the time range is invalid
        if start > end:
            return 0
        budgets = BudgetRepo.get_all()
        result = 0
        for budget in budgets:
            if budget.contains(start) and budget.contains(end):
                result += BudgetService.get_duration(start, end) * budget.daily_amount
            elif budget.after(start) and budget.by(end):
                result += budget.amount
            elif budget.contains(start):
                result += budget.amount - (start.day - 1) * budget.daily_amount
            elif budget.contains(end):
                result += end.day * budget.daily_amount
        return result

    @staticmethod
    def get_days_in_month(year, month) -> int:
        """

        :param year: int, ex. 2023
        :param month: int, ex. 7
        :return: int, ex. 31
        """
        return calendar.monthrange(year, month)[1]

    @staticmethod
    def get_duration(start: datetime, end: datetime) -> int:
        return (end - start).days + 1


class Budget:
    def __init__(self, year_month: str, amount: int) -> None:
        """

        :param year_month: str, ex. 20230715
        :param amount: int, ex. 10000
        """
        year = int(year_month[:4])
        month = int(year_month[4:])
        self.start = datetime(year, month, 1)
        days = BudgetService.get_days_in_month(year, month)
        self.end = datetime(year, month, days)
        self.amount = amount
        self.daily_amount = amount / days

    def contains(self, date: datetime) -> bool:
        """

        :param date: datetime, ex. datetime(2023, 7, 15)
        :return: bool, ex. True
        """
        return self.start <= date <= self.end

    def by(self, date: datetime) -> bool:
        """

        :param date: datetime, ex. datetime(2023, 7, 15)
        :return: bool, ex. True
        """
        return self.end <= date

    def after(self, date: datetime) -> bool:
        """

        :param date: datetime, ex. datetime(2023, 7, 15)
        :return: bool, ex. True
        """
        return self.start >= date


class BudgetRepo:
    @staticmethod
    def get_all() -> list[Budget]:
        """

        :return: list[Budget], ex. [Budget('202307', 3100), Budget('202308', 6200)]
        """
        return []
