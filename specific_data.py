import datetime
import time
import filter_data
from extract_data.extract import Extract
from export_data import ExportToData

start = time.time()

extractor = Extract()
exporter = ExportToData()

# calling kospi and kosdaq data using pykrx and OpenFinanceReader
kospi_kosdaq_data = extractor.get_data()

print("--------------")

# extract and calculating finance data recent 3 years data
extracted_data = extractor.extract_finance_data(
    [2020, 2021, 2022],
    # [2022],
    filter_data.filtering_data_that_specific_data(
        ['094970','332370', '086520'],
        # ['086520'],
        kospi_kosdaq_data
    ))

exporter.export_to_excel(
    f"/Users/yoodahun/Documents/Dahun Document/Investment information/{datetime.datetime.today().strftime('%Y%m%d')}_specific_data.xlsx",
    "specific_data",
    extracted_data
)




end = time.time()
sec = (end - start)

result_list = str(datetime.timedelta(seconds=sec)).split(".")
print(f"Total extracting time : {result_list[0]} ---------------------")