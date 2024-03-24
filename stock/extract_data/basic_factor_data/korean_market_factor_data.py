import datetime
import pandas as pd
import FinanceDataReader as fdr
import stock.filter_data as filter_data

from pykrx import stock


class KoreanMarketFactorData:
    def __init__(self):
        self.stock = stock
        self.fdr_data = fdr.StockListing("KRX-DESC")

    def get_kospi_market_data(self):
        """
        종목코드, 종목명, 업종, BPS, PER, PBR, EPS, DIV, DPS가 담긴 데이터를 리턴.
        :return: Pandas.DataFrame
        """
        return self.__get_fundamental_data("KOSPI")

    def get_kosdaq_market_data(self):
        """
        종목코드, 종목명, 업종, BPS, PER, PBR, EPS, DIV, DPS가 담긴 데이터를 리턴.
        :return: Pandas.DataFrame
        """
        return self.__get_fundamental_data("KOSDAQ")

    def get_stock_ticker_and_name_list(self, market):

        today = self.__get_date()

        return filter_data.drop_column(self.__get_korean_stock_ticker_and_name(today, market))

    def __get_fundamental_data(self, market):
        """
         종목코드, 종목명, 업종, 시가총액, 거래량, 거래대금, BPS, PER, PBR, EPS, DIV, DPS가 담긴 데이터를 리턴.
         :return: Pandas.DataFrame
         """
        today = self.__get_date()

        filtered_stock_ticker_and_name_list = filter_data.drop_column(
            self.__get_korean_stock_ticker_and_name(today, market))
        stock_cap = self.__get_fundamental_data_market_cap(today)

        temp_stock_list = pd.merge(filtered_stock_ticker_and_name_list, stock_cap, left_on="종목코드", right_on="종목코드")
        stock_fundamental = self.__get_korean_stock_fundamental(today, market)

        # 종목 코드로 조인
        return pd.merge(temp_stock_list, stock_fundamental, left_on="종목코드", right_on="종목코드")

    def __get_fundamental_data_market_cap(self, today):

        stock_list = self.stock.get_market_cap(today)
        stock_list = stock_list.reset_index()
        stock_list.rename(columns={'티커': '종목코드'}, inplace=True)

        return stock_list

    def __get_korean_stock_ticker_and_name(self, date, market):
        stock_list = pd.DataFrame({'종목코드': self.stock.get_market_ticker_list(date, market=market)})
        stock_list['종목명'] = stock_list['종목코드'].map(lambda x: stock.get_market_ticker_name(x))

        stock_list['업종'] = stock_list['종목명'].map(lambda x: self.__map_sector(x, self.fdr_data))

        return stock_list

    def __map_sector(self, x, fdr_data):
        try:
            result = fdr_data[fdr_data["Name"] == x]["Sector"].iloc[0]
        except IndexError:
            # IndexError가 발생하면 대체값으로 'Unknown'을 반환
            result = None

        return result


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
        today = datetime.datetime.today().strftime("%Y%m%d")
        year = str(datetime.datetime.today().strftime("%Y"))
        month = str(datetime.datetime.today().strftime("%m"))
        date = int(datetime.datetime.today().day)

        date_formated = datetime.datetime.strptime(today, "%Y%m%d")  # datetime format 으로 변환

        if date_formated.weekday() == 5:
            if month == '12':
                date -= 2  # 연말의 경우 2일을 뺀다.
            else:
                date -= 1  # 토요일일 경우 1일을 뺀다.
        elif date_formated.weekday() == 6:
            if month == '12':
                date -= 3  # 연말의 경우 3일을 뺀다.
            else:
                date -= 2  # 일요일일 경우 2일을 뺀다.
        elif date_formated.weekday() == 4 and month == '12':
            date -= 1  # 연말인데 금요일이면 1일을 뺀다.

            # 추석에 대한 처리
        if month == '09' and year == '2020':
            date -= 1
        elif month == '09' and year == '2023':
            date -= 3

        # print(year + month + str(date).zfill(2))
        # return '20230927'
        return year + month + str(date).zfill(2)
        # return '20220930'
