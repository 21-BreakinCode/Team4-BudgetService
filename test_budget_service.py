from datetime import datetime
from unittest import TestCase
from mock import patch

from budget_service import BudgetService, BudgetRepo, Budget


class TestBudgetService(TestCase):
    def setUp(self) -> None:
        '''Init budget table'''
        self.mock_multi_month_budget_list = [
            Budget('202306', 30),
            Budget('202307', 310),
            Budget('202308', 3100),
            Budget('202309', 3000),
            Budget('202310', 31),
        ]

        self.mock_empty_data_budget_list = [
            Budget('202306', 30),
            Budget('202308', 3100),
        ]

        self.mock_zero_budget_in_budget_list = [
            Budget('202306', 30),
            Budget('202307', 0),
            Budget('202308', 3100),
        ]

    @patch('budget_service.BudgetRepo.get_all', return_value = [Budget('202307', 3100)])
    def test_query_one_day_budget(self, mock_get_all):
        expected_budget = 100
        actual_budge = BudgetService.query(datetime(2023, 7, 15), datetime(2023, 7, 15))

        self.assertEqual(expected_budget, actual_budge)

    @patch('budget_service.BudgetRepo.get_all', return_value = [])
    def test_no_data(self, mock_get_all):
        expected_budget = 0
        actual_budge = BudgetService.query(datetime(2020, 7, 15), datetime(2020, 7, 15))

        self.assertEqual(expected_budget, actual_budge)

    @patch('budget_service.BudgetRepo.get_all', return_value = [Budget('202307', 3100)])
    def test_invalid_date(self, mock_get_all):
        expected_budget = 0
        actual_budge = BudgetService.query(datetime(2023, 7, 15), datetime(2023, 7, 12))

        self.assertEqual(expected_budget, actual_budge)

    @patch('budget_service.BudgetRepo.get_all', return_value = [Budget('202306', 30), Budget('202307', 310)])
    def test_overlap_months(self, mock_get_all):
        expected_budget = 12
        actual_budge = BudgetService.query(datetime(2023, 6, 29), datetime(2023, 7, 1))

        self.assertEqual(expected_budget, actual_budge)

    @patch('budget_service.BudgetRepo.get_all', return_value = [Budget('202308', 31), Budget('202306', 30), Budget('202307', 31)])
    def test_overlap_multi_months(self, mock_get_all):
        expected_budget = 38
        actual_budge = BudgetService.query(datetime(2023, 6, 29), datetime(2023, 8, 5))

        self.assertEqual(expected_budget, actual_budge)

    @patch('budget_service.BudgetRepo.get_all', return_value = [Budget('202308', 31), Budget('202306', 30), Budget('202307', 0)])
    def test_with_zero_budget_months(self, mock_get_all):
        expected_budget = 7
        actual_budge = BudgetService.query(datetime(2023, 6, 29), datetime(2023, 8, 5))

        self.assertEqual(expected_budget, actual_budge)

    @patch('budget_service.BudgetRepo.get_all', return_value = [Budget('202308', 31), Budget('202306', 30)])
    def test_skip_empty_month(self, mock_get_all):
        expected_budget = 7
        actual_budge = BudgetService.query(datetime(2023, 6, 29), datetime(2023, 8, 5))

        self.assertEqual(expected_budget, actual_budge)


