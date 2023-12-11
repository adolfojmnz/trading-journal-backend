from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from tests.utils.accounts import get_or_create_test_user

from tests.utils.trades import create_forex_trade_list


class MetricsMixin:
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_or_create_test_user()
        self.client.force_authenticate(user=self.user)
        return super().setUp()

    def test_trades_metrics(self):
        create_forex_trade_list(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_metrics)


class TestMetricssummaryEndpoint(MetricsMixin, TestCase):
    expected_metrics = {
        "net_profit": 75.0,
        "gross_profit": 114.0,
        "gross_loss": -39.0,
        "total_trades": 6,
        "total_profit_trades": 3,
        "total_loss_trades": 3,
        "average_profit": 38.0,
        "average_loss": -13.0,
        "profit_loss_ratio": 0.5,
        "loss_profit_ratio": 0.5,
        "average_holding_time": 6750.0,
        "average_position_volume": 0.01,
    }

    def setUp(self) -> None:
        self.url = reverse("metrics-summary")
        return super().setUp()


class TestPNLMetrics(MetricsMixin, TestCase):
    expected_metrics = {
        "net_profit": 75.0,
        "gross_profit": 114.0,
        "gross_loss": -39.0,
        "largest_profit": 60.0,
        "largest_loss": -14.7,
        "smallest_profit": 24.0,
        "smallest_loss": -9.6,
        "average_profit": 38.0,
        "average_loss": -13.0,
        "profit_loss_ratio": 0.5,
        "loss_profit_ratio": 0.5,
    }

    def setUp(self) -> None:
        self.url = reverse("metrics-pnl")
        return super().setUp()


class TestTotalTradesMetrics(MetricsMixin, TestCase):
    expected_metrics = {
        "total_trades": 6,
        "total_profit_trades": 3,
        "total_loss_trades": 3,
        "total_long_positions": 3,
        "total_short_positions": 3,
    }

    def setUp(self) -> None:
        self.url = reverse("metrics-totals")
        return super().setUp()


class TestHoldingTimeMetrics(MetricsMixin, TestCase):
    expected_metrics = {
        "average_holding_time": 6750.0,
        "average_holding_time_per_winning_trade": 6750.0,
        "average_holding_time_per_lossing_trade": 6750.0,
        "average_holding_time_per_long_position": 6750.0,
        "average_holding_time_per_short_position": 6750.0,
    }

    def setUp(self) -> None:
        self.url = reverse("metrics-holding-time")
        return super().setUp()


class TestPositionVolumeMetrics(MetricsMixin, TestCase):
    expected_metrics = {
        "min_position_volume": 0.01,
        "min_position_volume_per_winning_trade": 0.01,
        "min_position_volume_per_losing_trade": 0.01,
        "max_position_volume": 0.01,
        "max_position_volume_per_winning_trade": 0.01,
        "max_position_volume_per_losing_trade": 0.01,
        "average_position_volume": 0.01,
        "average_position_volume_per_long_position": 0.01,
        "average_position_volume_per_short_position": 0.01,
        "average_position_volume_per_winning_trade": 0.01,
        "average_position_volume_per_losing_trade": 0.01,
    }

    def setUp(self) -> None:
        self.url = reverse("metrics-volume")
        return super().setUp()
