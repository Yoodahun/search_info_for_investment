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

        result = self.__get_fundamental_data("KOSPI")
        return result

    def get_kosdaq_market_data(self):
        """
        종목코드, 종목명, 업종, BPS, PER, PBR, EPS, DIV, DPS가 담긴 데이터를 리턴.
        :return: Pandas.DataFrame
        """
        result = self.__get_fundamental_data("KOSDAQ")
        print(result.head(2))
        return result

    # def get_etf_market_data(self):
    #     etf_list = self.__get_korea_etf_ticker_and_name(self.__get_date())
    #     etf_fund = self.stock.get_etf_price_deviation(self.__get_date(), self.__get_date(),"309210")
    #     #
    #     # result = pd.merge(etf_list, stock_fund, left_on="종목코드", right_on="종목코드")
    #     print(etf_fund)

    def __get_korean_stock_ticker_and_name(self, date, market):
        stock_list = pd.DataFrame({'종목코드': self.stock.get_market_ticker_list(date, market=market)})
        stock_list['종목명'] = stock_list['종목코드'].map(lambda x: stock.get_market_ticker_name(x))
        stock_list['업종'] = stock_list['종목코드'].map(lambda x: SYMBOL_SECTOR_DIC[x])

        return stock_list

    def __get_korean_stock_fundamental(self, date, market):
        stock_fud = pd.DataFrame(self.stock.get_market_fundamental(date, market=market))
        stock_fud = stock_fud.reset_index()
        stock_fud.rename(columns={'티커': '종목코드'}, inplace=True)

        return stock_fud

    def __get_korea_etf_ticker_and_name(self, date):
        etf_list = pd.DataFrame({'종목코드': self.stock.get_etf_ticker_list(date)})
        etf_list['종목명'] = etf_list['종목코드'].map(lambda x: stock.get_etf_ticker_name(x))

        return etf_list

    def __get_date(self):
        """
        :return weekdays
        :return:
        """
        # date = datetime.datetime.now() - datetime.timedelta(days=1)
        today = datetime.datetime.today()
        check_date = today.weekday()
        if check_date == 5:
            today -= datetime.timedelta(days=1)
        elif check_date == 6:
            today -= datetime.timedelta(days=2)
        elif check_date == 0:
            today -= datetime.timedelta(days=3)

        return today.strftime("%Y%m%d")

    def __get_fundamental_data(self, market):
        """
         종목코드, 종목명, 업종, BPS, PER, PBR, EPS, DIV, DPS가 담긴 데이터를 리턴.
         :return: Pandas.DataFrame
         """
        today = self.__get_date()

        stock_list = self.__get_korean_stock_ticker_and_name(today, market)
        stock_fundamental = self.__get_korean_stock_fundamental(today, market)

        # 종목 코드로 조인
        return pd.merge(stock_list, stock_fundamental, left_on="종목코드", right_on="종목코드")
