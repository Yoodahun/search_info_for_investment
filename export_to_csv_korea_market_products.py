import FinanceDataReader as fdr
from kospi import kospi_ticker_list as KOSPI_LIST
from kosdaq import kosdaq_ticker_list as KOSDAQ_LIST
from etf import etf_ticker_list as ETF_LIST

save_file_path = "/Users/yoodahun/Documents/Dahun Document/Investment information/"

KRX = fdr.StockListing("KRX")

print_kospi = KRX[KRX['Symbol'].isin(KOSPI_LIST.KOSPI_MARKET_TICKER_LIST.keys())]
print_kosdaq = KRX[KRX['Symbol'].isin(KOSDAQ_LIST.KOSDAQ_MARKET_TICKER_LIST.keys())]
# print_etf = KRX[KRX['Symbol'].isin(ETF_LIST.ETF_TICKER_LIST.keys())]

print_kospi.to_csv(save_file_path + 'KOSPI_list.csv'
                   , encoding="cp949"
                   )
print_kosdaq.to_csv(save_file_path + 'KOSDAQ_list.csv'
                    , encoding="cp949"
                    )

KRX = fdr.StockListing("ETF/KR")
KRX.to_csv(save_file_path + 'KOREA_ETF_list_other.csv'
                 , encoding="cp949"
                 )