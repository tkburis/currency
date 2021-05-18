# import rates
from forex_python.converter import CurrencyRates
import datetime as dt
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import pandas as pd


class Grapher:
    c = CurrencyRates()

    def __init__(self, month_delta: int = 60):
        """
        :param month_delta: how long to go back
        """
        self.month_delta = month_delta

    def get_rates(self, currency_from: str, currency_to: str) -> pd.DataFrame:
        """
        Returns exchange rates monthly going back month_delta months
        :param currency_from: exchange rate from this
        :param currency_to: exchange rate to this
        :return: dataframe of exchange rates
        """
        now = dt.datetime.now()
        current_date = dt.datetime(now.year, now.month, 1) - relativedelta(months=self.month_delta)
        rates_list = []
        for month in range(self.month_delta):
            rate = self.c.get_rate(currency_from, currency_to, current_date)  # TODO: implement caching
            rates_list.append([current_date, rate])
            current_date = current_date + relativedelta(months=1)  # increment by 1 month
            print(f"{month+1} / {self.month_delta}")
        rates_df = pd.DataFrame(rates_list, columns=['Month', 'Rate'])  # convert to dataframe
        return rates_df

    def make_graph(self, currency_from: str, currency_to: str) -> None:
        """
        Displays graph of rates
        :param currency_from: exchange rate from this
        :param currency_to: exchange rate to this
        :return:
        """
        rates_df = self.get_rates(currency_from, currency_to)

        fig = plt.figure()
        fig.canvas.manager.set_window_title("Exchange Rate")

        plt.plot(rates_df['Month'], rates_df['Rate'], color='red', marker='o')
        plt.title('Exchange rate graph')
        plt.xlabel('Month')
        plt.ylabel(f'{currency_from} to {currency_to} rate')
        plt.grid(True)
        plt.show()
        return


if __name__ == "__main__":
    grapher = Grapher(month_delta=60)
    grapher.make_graph('USD', 'THB')
