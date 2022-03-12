import datetime

from factor_data import korean_market_factor_data


test = korean_market_factor_data.KoreanMarketFactorData()

test.get_kospi_market_data()

# dt = datetime.datetime.now()
# print(dt.strftime("%Y%m%d"))