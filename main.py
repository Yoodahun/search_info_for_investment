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
    filter_data.filtering_data_that_market_cap_under(0.33,
        kospi_kosdaq_data
    ))

exporter.export_to_excel_with_many_sheets(
    f"/Users/yoodahun/Documents/Dahun Document/Investment information/{datetime.datetime.today().strftime('%Y%m%d')}_screeningData.xlsx",
    [
        filter_data.filtering_low_per("ALL_DATA_저PER", kospi_kosdaq_data.copy()),
        filter_data.filtering_low_pbr_and_per("ALL_DATA_저PBR_저PER", 1.0, 10, kospi_kosdaq_data.copy(), True),
        filter_data.filtering_low_per("소형주_저PER", extracted_data.copy()),
        filter_data.filtering_low_pbr_and_per("소형주_저PBR_저PER", 1.0, 10, extracted_data.copy()),
        filter_data.filtering_low_psr_and_per("소형주_저PSR_저PER", 10, extracted_data.copy()),
        filter_data.filtering_peg("소형주_PEG", extracted_data.copy()),
        filter_data.filtering_high_div("고배당률_리스트", kospi_kosdaq_data.copy()),
        filter_data.filtering_high_propensity_to_dividend("소형주 고배당성향", extracted_data.copy()),
        filter_data.filtering_low_pfcr("소형주_저PFCR_시총잉여현금흐름", extracted_data.copy()),
        filter_data.filtering_low_pbr_and_high_gpa("소형주_저PBR_고GPA", 0.8, extracted_data.copy()),
        filter_data.filtering_high_ncav_cap_and_gpa("소형주_저NCAV_GPA_저부채비율", extracted_data.copy()),
        filter_data.filtering_profit_momentum("소형주_모멘텀_전분기대비_영업이익순이익_전략", extracted_data.copy()),
        filter_data.filtering_value_and_profit_momentum("소형주_밸류모멘텀_전략", extracted_data.copy()),
        filter_data.filtering_value_factor("소형주_HIGH_SCORE_Four_value", extracted_data.copy()),
        filter_data.filtering_value_factor2("소형주_10가지_팩터순위합계", extracted_data.copy()),
        filter_data.filtering_value_factor_upgrade("소형주_강환국_슈퍼가치전략_업글", extracted_data.copy()),
        # filter_data.filtering_value_and_quality("소형주_저PBR_고GPA_자산성장률계산", 1.0, extracted_data.copy()),
        filter_data.filtering_new_F_score_and_low_pbr("소형주_NEW F Score and Low PBR", extracted_data.copy()),

        ("Extracted_RAW_Data", extracted_data),
        ("RAW_Data", kospi_kosdaq_data)
    ]
)

end = time.time()
sec = (end - start)

result_list = str(datetime.timedelta(seconds=sec)).split(".")
print(f"Total extracting time : {result_list[0]} ---------------------")
