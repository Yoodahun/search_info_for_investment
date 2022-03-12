import datetime
import pandas as pd

from pykrx import stock
from const.sector import SYMBOL_SECTOR_DIC


class KoreanMarketFactorData:
    def __init__(self):
        self.stock = stock

    def get_kospi_market_data(self):
        """
        종목코드, 종목명, 업종, BPS, PER, PBR, EPS, DIV, DPS가 담긴 데이터를 리턴.
        :return: Pandas.DataFrame
        """

        result = self.get_fundamental_data("KOSPI")
        print(result.head(2))

    def get_kosdaq_market_data(self):
        """
        종목코드, 종목명, 업종, BPS, PER, PBR, EPS, DIV, DPS가 담긴 데이터를 리턴.
        :return: Pandas.DataFrame
        """
        result = self.get_fundamental_data("KOSDAQ")
        print(result.head(2))

    def get_etf_market_data(self):
        pass

    def get_korean_stock_ticker_and_name(self, date, market):
        stock_list = pd.DataFrame({'종목코드': self.stock.get_market_ticker_list(date, market=market)})
        stock_list['종목명'] = stock_list['종목코드'].map(lambda x: stock.get_market_ticker_name(x))
        stock_list['업종'] = stock_list['종목코드'].map(lambda x: SYMBOL_SECTOR_DIC[x])

        return stock_list

    def get_korean_stock_fundamental(self, date, market):
        stock_fud = pd.DataFrame(self.stock.get_market_fundamental(date, market=market))
        stock_fud = stock_fud.reset_index()
        stock_fud.rename(columns={'티커': '종목코드'}, inplace=True)

        return stock_fud

    def get_date(self):
        """
        :return yesterday
        :return:
        """
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        return date.strftime("%Y%m%d")

    def get_fundamental_data(self, market):
        """
         종목코드, 종목명, 업종, BPS, PER, PBR, EPS, DIV, DPS가 담긴 데이터를 리턴.
         :return: Pandas.DataFrame
         """
        today = self.get_date()

        stock_list = self.get_korean_stock_ticker_and_name(today, market)
        stock_fundamental = self.get_korean_stock_fundamental(today, market)

        # 종목 코드로 조인
        return pd.merge(stock_list, stock_fundamental, left_on="종목코드", right_on="종목코드")
