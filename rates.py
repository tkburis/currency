from forex_python.converter import CurrencyRates

c = CurrencyRates()


def convert_currency(currency_from, currency_to, value) -> float:
    rate = float(c.get_rate(currency_from, currency_to))
    converted = round(value * rate, 2)
    return converted


def get_all_currencies() -> list:
    rates = c.get_rates('USD')
    currencies = []
    for code, rate in rates.items():
        currencies.append(code)
    currencies = sorted(currencies)
    return currencies


if __name__ == "__main__":
    print(get_all_currencies())
