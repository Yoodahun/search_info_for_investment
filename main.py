import datetime
import time

import filter_data
from extract_data.extract import Extract
from export_data import ExportToData


"""
condition = {
    'PBR': 0.8,
    'PER': 10,
    'DIV': 5.0
}
"""

#


start = time.time()
extractor = Extract()
exporter = ExportToData()
kospi_kosdaq_data = extractor.get_data()
print(kospi_kosdaq_data)
extracted_data = extractor.extract_finance_data(kospi_kosdaq_data)

# KOSDAQ_LOW_PBR_AND_PER = extractor.filter_low_pbr_and_per(1.0, 10, kosdaq_data)

# exporter.export_to_excel("/Users/yoodahun/Documents/Dahun Document/Investment information/total.xlsx", kospi_kosdaq_data)
exporter.export_to_excel("/Users/yoodahun/Documents/Dahun Document/Investment information/filtered.xlsx",
                         filter_data.filtering_data_that_market_cap_under_thirty_percent(kospi_kosdaq_data)
                         )


exporter.export_to_excel_with_many_sheets(
    "/Users/yoodahun/Documents/Dahun Document/Investment information/screeningData.xlsx",
    [
        filter_data.filtering_low_pbr_and_per(0.8,10, extracted_data)
    ]
)

end = time.time()
sec = (end - start)

result_list = str(datetime.timedelta(seconds=sec)).split(".")
print(f"Total extracting time : {result_list[0]} ---------------------")

