from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from accounts.utils import create_test_user

from trades.helpers.test_utils import create_forex_trade_list


class TestTradesMetricsEndpoint(TestCase):

    expected_metrics = {
        "net_profit": 75.0,
        "gross_profit": 114.0,
        "gross_loss": -39.0,
        "total_trades": 6,
        "total_profit_trades": 3,
        "total_loss_trades": 3,
        "largest_profit_trade": 60.0,
        "largest_loss_trade": -14.7,
        "smallest_profit_trade": 24.0,
        "smallest_loss_trade": -9.6,
        "average_profit_trade": 38.0,
        "average_loss_trade": -13.0,
        "percentage_profit_trades": 50.0,
        "percentage_loss_trades": 50.0,
        "total_long_positions": 3,
        "total_short_positions": 3,
        "average_holding_time": 6750.0,
        "average_holding_time_per_winning_trade": 6900.0,
        "average_holding_time_per_lossing_trade": 6600.0,
        "average_holding_time_per_long_position": 5400.0,
        "average_holding_time_per_short_position": 8100.0,
    }

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_test_user()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("trades-metrics")
        return super().setUp()

    def test_trades_metrics(self):
        create_forex_trade_list(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_metrics)