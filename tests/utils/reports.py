from countries.models import EconomicReport

from tests.utils.indicators import (
    get_or_create_us_economic_indicator,
    get_or_create_uk_economic_indicator,
)


def get_or_create_us_economic_report():
    indicator = get_or_create_us_economic_indicator()
    return EconomicReport.objects.get_or_create(
        name="ADP Employment Change(Nov)",
        description="...",
        impact_level=3,
        datetime="2023-12-06T09:15:00.00Z",
        economic_indicator=indicator,
        actual=103000,
        forecast=130000,
        previous=106000,
    )[0]


def get_or_create_uk_economic_report():
    indicator = get_or_create_uk_economic_indicator()
    return EconomicReport.objects.get_or_create(
        name="Relased of Unemployment Rate (YoY)",
        description="...",
        impact_level=3,
        datetime="2023-12-12T12:00:00.00Z",
        economic_indicator=indicator,
        unit="%",
        actual=5.5,
        forecast=4.5,
        previous=5.5,
    )


def get_or_create_economic_report_list():
    reports = [
        get_or_create_us_economic_report(),
        get_or_create_uk_economic_report(),
    ]
    return reports
