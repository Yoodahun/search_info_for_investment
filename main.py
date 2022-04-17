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
extracted_data = extractor.extract_finance_data(filter_data.filtering_data_that_market_cap_under_thirty_percent(
    kospi_kosdaq_data.copy()
))

# KOSDAQ_LOW_PBR_AND_PER = extractor.filter_low_pbr_and_per(1.0, 10, kosdaq_data)

# exporter.export_to_excel("/Users/yoodahun/Documents/Dahun Document/Investment information/total.xlsx", kospi_kosdaq_data)
exporter.export_to_excel("/Users/yoodahun/Documents/Dahun Document/Investment information/filtered.xlsx",
                         filter_data.filtering_data_that_market_cap_under_thirty_percent(kospi_kosdaq_data)
                         )


exporter.export_to_excel_with_many_sheets(
    "/Users/yoodahun/Documents/Dahun Document/Investment information/screeningData.xlsx",
    [
        filter_data.filtering_low_per_that_all_data(kospi_kosdaq_data.copy()),
        filter_data.filtering_high_div_that_all_data(kospi_kosdaq_data.copy()),
        filter_data.filtering_low_pfcr(extracted_data.copy()),
        filter_data.filtering_low_pbr_and_per(1.0,10, extracted_data.copy()),
        filter_data.filtering_low_pbr_and_high_gpa(0.8, extracted_data.copy()),
        filter_data.filtering_high_ncav_cap_and_gpa(extracted_data.copy()),
        filter_data.filtering_profit_momentum(extracted_data.copy()),
        filter_data.filtering_value_and_profit_momentum(extracted_data.copy()),
        filter_data.filtering_value_factor(extracted_data.copy()),
        filter_data.filtering_value_factor_upgrade(extracted_data.copy()),
        filter_data.filtering_value_and_quality(1.0, extracted_data.copy()),
        filter_data.filtering_new_F_score_and_low_pbr(extracted_data.copy()),

        ("Extracted_RAW_Data", extracted_data),
        ("RAW_Data", kospi_kosdaq_data)
    ]
)

end = time.time()
sec = (end - start)

result_list = str(datetime.timedelta(seconds=sec)).split(".")
print(f"Total extracting time : {result_list[0]} ---------------------")

