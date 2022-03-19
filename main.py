import datetime
import time
import openpyxl
from pykrx import stock
import pandas as pd

from extract_data.extract import Extract
from extract_data.basic_factor_data import korean_market_factor_data

# test1 = korean_market_factor_data.KoreanMarketFactorData()

# test1.get_kospi_market_data()
# test1.get_etf_market_data()
# test2 = extract.low_pbr_and_per("KOSPI")
# print(test2.head(2))

# pd.set_option('display.max_columns', None)
# test = stock.get_market_fundamental_by_date("20220317", "20220318", "005930")
# test = test.reset_index()
# print(test)
#



start = time.time()
extractor = Extract()
# test3 = extractor.filter_high_div_and_dps("KOSPI")
test3 = extractor.filter_low_pbr_and_per(market="KOSPI")
test3.to_excel("/Users/yoodahun/Documents/Dahun Document/Investment information/test4_excel_file.xlsx", encoding="cp949"
                   )
end = time.time()
sec =(end - start)

result_list = str(datetime.timedelta(seconds=sec)).split(".")
print(result_list[0])


# print(test3.head(10))

# dt = datetime.datetime.now()
# print(dt.strftime("%Y%m%d"))