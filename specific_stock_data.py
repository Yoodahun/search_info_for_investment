import datetime
import time
import stock.filter_data as filter_data
from stock.extract_data.extract import Extract
from export_data import ExportToData

start = time.time()

extractor = Extract()
exporter = ExportToData()

# calling kospi and kosdaq data using pykrx and OpenFinanceReader
kospi_kosdaq_data = extractor.get_data()

print("--------------")

# extract and calculating finance data recent 3 years data
extracted_data = extractor.extract_finance_data(
    [2021, 2022, 2023],
    # [2022],
    filter_data.filtering_data_that_specific_data([
    '001800',
    '001940',
    '002030',
    '007860',
    '009300',
    '009970',
    '017940',
    '023910',
    '054040',
    '096760',
'328130'
    ],
        kospi_kosdaq_data
    ))

exporter.export_to_excel(
    f"/Users/yoodahun/Documents/Investment information/{datetime.datetime.today().strftime('%Y%m%d')}_specific_data.xlsx",
    "specific_data",
    extracted_data
)




end = time.time()
sec = (end - start)

result_list = str(datetime.timedelta(seconds=sec)).split(".")
print(f"Total extracting time : {result_list[0]} ---------------------")