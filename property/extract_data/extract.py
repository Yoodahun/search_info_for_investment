from property.const.district_converter import DistrictConverter
from config.api_key import PUBLIC_DATA_PORTAL
import pandas as pd
import PublicDataReader as pdr

converter = DistrictConverter()
API = pdr.Transaction(PUBLIC_DATA_PORTAL, debug=False)

header = [
    "시도",
    "시군구",
    "법정동",
    "도로명",
    "지번",
    "종류",
    "아파트",
    "건축년도",
    "전용면적",
    "전용면적(평)",
    "거래년도",
    "거래월",
    "거래일",
    "거래금액",
    "일련번호",
    "거래유형",
    "중개사소재지",
    "해제여부",
    "해제사유발생일"

]

product_list = {
    "아파트":"아파트",
    "연립다세대": "다세대빌라",
    "단독다가구":"단독다가구",
    "오피스텔": "오피스텔"
}


def get_test_data(product, transaction, year_month):
    seoul_name = converter.get_si_do_name("서울")

    df = pd.DataFrame()

    data = get_data_from_portal(product, transaction, "11740", year_month)
    data["시도"] = seoul_name
    data["시군구"] = "강동구"
    df = pd.concat([data, df])

    df = caculate_column_data(df)

    df.rename(columns={"년": "거래년",
                       "월": "거래월",
                       "일": "거래일"
                       },
              inplace=True)
    return df.reindex(columns=header)


def get_seoul_data(transaction, year_month):
    seoul_code = converter.get_si_do_code("서울")
    seoul_name = converter.get_si_do_name("서울")
    sigungu_list = converter.get_sigungu(seoul_code)

    apart_data = get_apartment_data(seoul_name, sigungu_list, transaction, year_month)
    villa_data = get_villa_data(seoul_name, sigungu_list, transaction, year_month)

    df = pd.concat([apart_data, villa_data])

    return df.reset_index().reindex(columns=header)

def get_district_data(sido_name, sigungu_name, transaction, year_month):
    si_do_name = converter.get_si_do_name(sido_name)
    si_do_code = converter.get_si_do_code(si_do_name)
    sigungu_list = converter.get_sigungu_list(si_do_code, sigungu_name)

    apart_data = get_apartment_data(si_do_name, sigungu_list, transaction, year_month)
    villa_data = get_villa_data(si_do_code, sigungu_list, transaction, year_month)

    df = pd.concat([apart_data, villa_data])

    return df.reset_index().reindex(columns=header)


def get_apartment_data(sido_name, sigungu_list, transaction, year_month):
    return get_data_using_sigungu_list(sido_name, sigungu_list, "연립다세대", transaction, year_month)


def get_villa_data(sido_name, sigungu_list, transaction, year_month):
    return get_data_using_sigungu_list(sido_name, sigungu_list, "아파트", transaction, year_month)




def get_data_using_sigungu_list(si_do_name, sigungu_list: list, product, transaction, year_month):
    df = pd.DataFrame()

    for sigungu in sigungu_list:
        print(f"{si_do_name} / {sigungu['sigungu_name']} {product} 조회")
        data = get_data_from_portal(product, transaction, sigungu["sigungu_code"], year_month)
        data["시도"] = si_do_name
        data["시군구"] = sigungu["sigungu_name"]
        data["종류"] = product_list[product]
        df = pd.concat([data, df])

    df = caculate_column_data(df)

    df.rename(columns={"년": "거래년도",
                       "월": "거래월",
                       "일": "거래일"
                       },
              inplace=True)

    return df


def caculate_column_data(df: pd.DataFrame):
    df["전용면적(평)"] = round(df["전용면적"] / 3.3, 1)

    return df


def get_data_from_portal(proudct, transaction, sigungu_code, year_month):
    return API.read_data(proudct, transaction, sigungu_code, year_month)
