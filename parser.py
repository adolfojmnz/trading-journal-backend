import csv

from trades.models import Trade

from assets.models import Currency, CurrencyPair


def format_datetime(timestring):
    """Converts the timestring to ISO format"""
    date = timestring.split(" ")[0].split(".")
    time = timestring.split(" ")[1]
    return f"{date[0]}-{date[1]}-{date[2]} {time}"


def load_trades_from_csv(file_path, user):
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row.

        operations = []
        for row in reader:
            try:
                operation = Trade(
                    user=user,
                    ticket=int(row[0]),
                    type="S" if row[2] == "sell" else "L",
                    currency_pair=CurrencyPair.objects.get(symbol__iexact=row[4]),
                    open_datetime=format_datetime(row[1]),
                    close_datetime=format_datetime(row[8]),
                    open_price=float(row[5]),
                    stop_loss=float(row[6]),
                    take_profit=float(row[7]),
                    close_price=float(row[9]),
                    volume=float(row[3]),
                    pnl=float(row[10]),
                )
                operations.append(operation)
            except:
                continue
        Trade.objects.bulk_create(operations)


def load_currencies_from_csv(file_path):
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row.

        currencies = []
        for row in reader:
            try:
                currency = Currency(
                    symbol=row[0],
                    name=row[1],
                    description=row[2],
                )
                currencies.append(currency)
            except:
                continue
        Currency.objects.bulk_create(currencies)


def load_currency_pairs_from_csv(file_path):
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row.

        pairs = []
        for row in reader:
            try:
                pair = CurrencyPair(
                    symbol=row[0],
                    base_currency=Currency.objects.get(symbol__iexact=row[1]),
                    quote_currency=Currency.objects.get(symbol__iexact=row[2]),
                    pip_decimal_position=int(row[3]),
                )
                pairs.append(pair)
            except:
                continue
        CurrencyPair.objects.bulk_create(pairs)
