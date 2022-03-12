import datetime
import pykrx.stock


class ExportToCSVKoreaMarketProducts:
    stock_getter = pykrx.stock

    def print_dictionary(self):
        self.__print_korean_market_dictionary("KOSPI")
        self.__print_korean_market_dictionary("KOSDAQ")
        self.__print_korean_eth_dictionary()

    def __print_korean_market_dictionary(self, market_name):
        MARKET_TICKER_LIST = {}
        tickers = self.stock_getter.get_market_ticker_list(str(datetime.datetime.today()), market=market_name)
        for ticker_number in tickers:
            MARKET_TICKER_LIST[ticker_number] = pykrx.stock.get_market_ticker_name(ticker_number)

        print(MARKET_TICKER_LIST)

    def __print_korean_eth_dictionary(self):
        MARKET_TICKER_LIST = {}
        tickers = self.stock_getter.get_etf_ticker_list(str(datetime.datetime.today()))
        for ticker_number in tickers:
            MARKET_TICKER_LIST[ticker_number] = pykrx.stock.get_etf_ticker_name(ticker_number)

        print(MARKET_TICKER_LIST)


ExportToCSVKoreaMarketProducts().print_dictionary()
