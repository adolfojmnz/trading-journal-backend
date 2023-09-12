"""
    The purpose of this data is to be used to ppopulate
    the database upon the project set up.
"""

simple_user = {
    "username": "johnd",
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@localhost.com",
    "password": "johnd#pass",
}

trading_account = {
    "broker": "Demo Broker Corp",
    "type": "DM",
    "equity": 100,
}

currencies = {
    "eur": {
        "symbol": "EUR",
        "name": "Euro",
        "description": "Official currency of 20 of the 27 nations of the EU",
    },
    "gbp": {
        "symbol": "GBP",
        "name": "Great Britain Pound",
        "description": "Official currency of the United Kingdom",
    },
    "jpy": {
        "symbol": "JPY",
        "name": "Japanese Yen",
        "description": "Official currency of Japan",
    },
}