import datetime
import time
from stock.extract_data.extract import Extract
import pandas as pd
import pystocklib.srim as srim
from export_data import ExportToData


def calculate_company_value(net_worth, roe, k, discount_roe=1.0):
    if discount_roe == 1.0:
        value = net_worth + (net_worth * (roe - k)) / k
    else:
        excess_earning = net_worth * (roe - k) * 0.01
        mul = discount_roe / (1.0 + k * 0.01 - discount_roe)
        value = net_worth + excess_earning * mul

    return value


start = time.time()
extractor = Extract()
exporter = ExportToData()

kospi_data = extractor.factor_data.get_stock_ticker_and_name_list("KOSPI")
kosdaq_data = extractor.factor_data.get_stock_ticker_and_name_list("KOSDAQ")

kospi_kosdaq_data = pd.concat([kospi_data, kosdaq_data])

net_worth_and_roe_list = kospi_kosdaq_data[["종목코드"]]
net_worth_and_roe_list.reset_index(drop=True, inplace=True)
require_rate_of_return = [1.0, 0.9, 0.8]

for i in range(len(net_worth_and_roe_list)):
    print(f'{net_worth_and_roe_list.loc[i, "종목코드"]}, {i + 1}/{len(net_worth_and_roe_list.index.values.tolist())}')

    s_rim_values = []

    try:
        net_worth = srim.reader.get_net_worth(net_worth_and_roe_list.loc[i, "종목코드"])
    except:
        net_worth = 0

    try:
        roe = srim.reader.get_roe(net_worth_and_roe_list.loc[i, "종목코드"])
    except:
        roe = 0

    for discount_roe in require_rate_of_return:
        s_rim_values.append(calculate_company_value(net_worth, roe, 10, discount_roe))

    net_worth_and_roe_list.loc[i, "net_worth"] = net_worth
    net_worth_and_roe_list.loc[i, "average_roe"] = roe
    net_worth_and_roe_list.loc[i, "s-rim_value_1"] = s_rim_values[0]
    net_worth_and_roe_list.loc[i, "s-rim_value_2"] = s_rim_values[1]
    net_worth_and_roe_list.loc[i, "s-rim_value_3"] = s_rim_values[2]

exporter.export_to_excel(
    "stock/crawling_data/net_worth_and_roe_list_for_s_rim.xlsx",
    "s_rim",
    net_worth_and_roe_list
)

end = time.time()
sec = (end - start)

result_list = str(datetime.timedelta(seconds=sec)).split(".")
print(f"Total extracting time : {result_list[0]} ---------------------")
