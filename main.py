import datetime

from extract_data import extract
from extract_data.factor_data import korean_market_factor_data

# test1 = korean_market_factor_data.KoreanMarketFactorData()

# test1.get_kospi_market_data()
# test1.get_etf_market_data()
# test2 = extract.low_pbr_and_per("KOSPI")
# print(test2.head(2))
#
test3 = extract.filter_high_div_and_dps("KOSPI")
print(test3.head(2))

# dt = datetime.datetime.now()
# print(dt.strftime("%Y%m%d"))