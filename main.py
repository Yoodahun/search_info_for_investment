import datetime
import time

import stock.filter_data as filter_data
from stock.extract_data.extract import Extract
from export_data import ExportToData

years = [2021, 2022, 2023]


def filterging_data(choice, data):
    if choice == 1:
        return filter_data.filtering_data_that_market_cap_under(0.3, data)
    else:
        return filter_data.filtering_data_that_market_cap_greater_than(0.8, data)


def export_data(category, raw_data, extracted_data):
    exporter = ExportToData()

    exporter.export_to_excel_with_many_sheets(
        f"/Users/yoodahun/Documents/Investment information/{datetime.datetime.today().strftime('%Y%m%d')}_{category}_screeningData.xlsx",
        [
            filter_data.filtering_low_per("ALL_DATA_저PER", raw_data.copy(), True),
            filter_data.filtering_low_pbr_and_per("ALL_DATA_저PBR_저PER", 1.0, 10, raw_data.copy(), True),
            filter_data.filtering_s_rim_disparity_all_data("S-RIM ALL_DATA", raw_data.copy()),
            filter_data.filtering_low_per(f"{category}_저PER", extracted_data.copy()),
            filter_data.filtering_low_pbr_and_per(f"{category}_저PBR_저PER", 1.0, 10, extracted_data.copy()),
            filter_data.filtering_low_psr_and_per(f"{category}_저PSR_저PER", 10, extracted_data.copy()),
            filter_data.filtering_peg(f"{category}_PEG", extracted_data.copy()),
            filter_data.filtering_high_div("고배당률_리스트", raw_data.copy()),
            filter_data.filtering_high_propensity_to_dividend(f"{category}_고배당성향", extracted_data.copy()),
            filter_data.filtering_low_pfcr(f"{category}_저PFCR_시총잉여현금흐름", extracted_data.copy()),
            filter_data.filtering_low_pbr_and_high_gpa(f"{category}_저PBR_고GPA", 0.8, extracted_data.copy()),
            filter_data.filtering_high_ncav_cap_and_gpa(f"{category}_고NCAV_GPA_저부채비율", extracted_data.copy()),
            filter_data.filtering_s_rim_disparity_and_high_nav(f"{category}_S-RIM_괴리율_고NAV", extracted_data.copy()),
            filter_data.filtering_profit_momentum(f"{category}_모멘텀_전분기대비_영업이익순이익_전략", extracted_data.copy()),
            filter_data.filtering_value_factor(f"{category}_슈퍼가치_4가지_전략", extracted_data.copy()),
            filter_data.filtering_value_and_profit_momentum(f"{category}_성장주모멘텀_전략", extracted_data.copy()),
            filter_data.filtering_value_factor3(f"{category}_6가지_팩터순위합계", extracted_data.copy()),
            filter_data.filtering_value_factor2(f"{category}_12가지_팩터순위합계", extracted_data.copy()),
            filter_data.filtering_value_factor_upgrade(f"{category}_강환국_슈퍼가치전략_업글", extracted_data.copy()),
            # filter_data.filtering_value_and_quality("소형주_저PBR_고GPA_자산성장률계산", 1.0, extracted_data.copy()),
            # filter_data.filtering_new_F_score_and_low_pbr("소형주_NEW F Score and Low PBR", extracted_data.copy()),

            ("Extracted_RAW_Data", extracted_data),
            ("RAW_Data", raw_data)
        ]
    )


def main():
    choice = int(input("소형주 : 1 / 대형주 : 2 를 입력하세요."))

    start = time.time()

    extractor = Extract()

    # calling kospi and kosdaq data using pykrx and OpenFinanceReader
    kospi_kosdaq_data = extractor.get_data()

    print("--------------")

    # extract and calculating finance data recent 3 years data

    if choice == 1:
        print("소형주 스크래핑을 시작합니다 -------")
        extracted_data = extractor.extract_finance_data(
            years,
            filterging_data(1, kospi_kosdaq_data)
        )
        export_data("소형주", kospi_kosdaq_data, extracted_data)
    else:
        print("대형주 스크래핑을 시작합니다 -------")
        extracted_data = extractor.extract_finance_data(
            years,
            filterging_data(2, kospi_kosdaq_data)
        )
        export_data("대형주", kospi_kosdaq_data, extracted_data)

    end = time.time()
    sec = (end - start)

    result_list = str(datetime.timedelta(seconds=sec)).split(".")
    print(f"Total extracting time : {result_list[0]} ---------------------")


if __name__ == "__main__":
    main()
