def get_condition1(df):
    # 유동자산
    return (df.sj_nm == '재무상태표') & ((df.account_nm == '유동자산') | (df.account_nm == 'II. 유동자산') |
                                    (df.account_nm == 'Ⅰ.유동자산') | (df.account_nm == '유동자산 합계') | (
                                            df.account_nm == 'I.유동자산') |
                                    (df.account_nm == 'I. 유동자산') | (df.account_nm == 'l. 유동자산'))  # 유동자산


def get_condition2(df):
    # 부채총계
    return (df.sj_nm == '재무상태표') & ((df.account_nm == '부채총계') | (df.account_nm == '부  채  총  계') |
                                    (df.account_nm == '부채 총계') | (df.account_nm == '부    채    총    계')
                                    )  # 부채총계


def get_condition3(df):
    # 자본 총계
    return (df.sj_nm == '재무상태표') & \
           ((df.account_nm == '자본총계') | (df.account_nm == '반기말자본') | (df.account_nm == '3분기말자본') |
            (df.account_nm == '분기말자본') | (df.account_nm == '1분기말자본') | (df.account_nm == '자  본  총  계') |
            (df.account_nm == '기말') | (df.account_nm == '자본 총계') | (df.account_nm == '기말자본 잔액') |
            (df.account_nm == '분기말') | (df.account_nm == '반기말') | (df.account_nm == '자 본 총 계') |
            (df.account_nm == '분기말 잔액') | (df.account_nm == '반기말 잔액') | (df.account_nm == '자    본    총    계')
            )  # 자본총계


def get_condition4(df):
    # 매출액 부분
    return ((df.sj_nm == '손익계산서') | (df.sj_nm == '포괄손익계산서')) & (
            (df.account_nm == '매출액') | (df.account_nm == '수익(매출액)') | (df.account_nm == '매출') |
            (df.account_nm == '영업수익') |(df.account_nm == '수익') | (df.account_nm == '영업수익(매출액)') |
            (df.account_nm == 'Ⅰ.매출') |(df.account_nm == 'I.매출액') | (df.account_nm == 'Ⅰ.매출액') |
            (df.account_nm == 'I. 매출액') | (df.account_nm == '매출액(영업수익)') | (df.account_nm == 'I. 영업수익') |
            (df.account_nm == 'I. 영업수익')
    )


def get_condition5(df):
    # 매출총이익
    return ((df.sj_nm == '손익계산서') | (df.sj_nm == '포괄손익계산서')) & \
           (
                   (df.account_nm == '매출총이익') | (df.account_nm == '매출 총이익') |
                   (df.account_nm == '매출총이익(손실)') | (df.account_nm == 'Ⅲ.매출총이익') |
                   (df.account_nm == 'III.매출총이익') | (df.account_nm == 'Ⅲ.매출총이익') |
                   (df.account_nm == 'III. 매출총이익(손실)') | (df.account_nm == 'III. 매출총이익') |
                   (df.account_nm == '매출총이익(영업수익)') | (df.account_nm == 'II.재료비')
           )


def get_condition6(df):
    # 영업이익, 영업손실
    return ((df.sj_nm == '손익계산서') | (df.sj_nm == '포괄손익계산서')) & \
           ((df.account_nm == '영업이익(손실)') | (df.account_nm == '영업이익') |
            (df.account_nm == '영업손실(이익)') | (df.account_nm == '영업손익') |
            (df.account_nm == '계속영업이익(손실)') | (df.account_nm == 'Ⅳ.영업이익') |
            (df.account_nm == 'VI.영업이익(손실)') | (df.account_nm == 'V.영업이익') | (df.account_nm == 'V. 영업이익(손실)') |
            (df.account_nm == 'IV. 영업이익') | (df.account_nm == '영업이익 (손실)') | (df.account_nm == '영업손실') |
            (df.account_nm == 'IV. 영업이익(손실)') | (df.account_nm == '정상영업손익') | (df.account_nm == 'III. 영업손실') |
            (df.account_nm == 'III. 영업이익') | (df.account_nm == 'III. 영업이익(손실)')
            )



def get_condition7(df):
    # 당기 순 이익
    return ((df.sj_nm == '손익계산서') | (df.sj_nm == '포괄손익계산서') | (df.sj_nm == '현금흐름표')) & \
           ((df.account_nm == '당기순이익(손실)') | (df.account_nm == '당기순이익') |
            (df.account_nm == '분기순이익') | (df.account_nm == '분기순이익(손실)') | (df.account_nm == '반기순이익') |
            (df.account_nm == '반기순이익(손실)') | (df.account_nm == '연결분기순이익') | (df.account_nm == '연결반기순이익') |
            (df.account_nm == '연결당기순이익') | (df.account_nm == '연결분기(당기)순이익') | (df.account_nm == '연결반기(당기)순이익') |
            (df.account_nm == '연결분기순이익(손실)') | (df.account_nm == '당기순손익') | (df.account_nm == 'Ⅶ.당기순이익') |
            (df.account_nm == 'VIII.당기순이익(손실)') | (df.account_nm == 'XIII. 당기순이익(손실)') | (
                    df.account_nm == '반기연결순이익(손실)') |
            (df.account_nm == '연결당기순이익(손실)') | (df.account_nm == '당기의 순이익') | (df.account_nm == '분기기순이익(손실)') |
            (df.account_nm == '분기순손익') | (df.account_nm == '분기순손실') | (df.account_nm == '반기순손익') | (df.account_nm == '분기연결순손실') |
            (df.account_nm == '분기연결순이익(손실)') | (df.account_nm == 'VI. 당기순이익(손실)') | (df.account_nm == '연결반기순이익(손실)') |
            (df.account_nm == 'IX. 반기순손실') | (df.account_nm == 'IX. 반기순이익')
            )


# 현금흐름표 부분
def get_condition8(df):
    ## 영업활동 현금흐름
    return (df.sj_nm == '현금흐름표') & ((df.account_nm == '영업활동으로 인한 현금흐름') | (df.account_nm == '영업활동 현금흐름') |
                                    (df.account_nm == '영업활동현금흐름') | (df.account_nm == '영업활동으로인한 현금흐름') | (
                                            df.account_nm == '영업활동으로인한순현금흐름') |
                                    (df.account_nm == 'Ⅰ. 영업활동으로 인한 현금흐름') | (df.account_nm == 'I.영업활동현금흐름') | (
                                            df.account_nm == '영업활동으로인한현금흐름') |
                                    (df.account_nm == '영업활동으로 인한 순현금흐름') | (df.account_nm == '영업활동으로인한 순현금흐름') | (
                                            df.account_nm == '1.영업활동현금흐름') |
                                    (df.account_nm == 'Ⅰ.영업활동현금흐름') | (df.account_nm == '영업활동으로 인한 현금 흐름') | (
                                            df.account_nm == 'I. 영업활동현금흐름') |
                                    (df.account_nm == 'I. 영업활동으로 인한 현금흐름') | (df.account_nm == 'I.영업활동으로 인한 현금흐름') |
                                    (df.account_nm == '영업활동순현금흐름 합계') | (df.account_nm == 'Ⅰ. 영업활동현금흐름') |
                                    (df.account_nm == '영업으로부터 창출된 현금흐름') | (df.account_nm == 'Ⅰ. 영업활동으로 인한 순현금흐름'))


def get_condition9(df):
    # 투자활동으로인한 현금흐름
    return (df.sj_nm == '현금흐름표') & ((df.account_nm == '투자활동으로 인한 현금흐름') | (df.account_nm == '투자활동 현금흐름') |
                                    (df.account_nm == '투자활동현금흐름') | (df.account_nm == '투자활동으로인한 현금흐름') | (
                                            df.account_nm == '투자활동으로인한순현금흐름') |
                                    (df.account_nm == 'Ⅱ. 투자활동으로 인한 현금흐름') | (df.account_nm == 'II.투자활동현금흐름') | (
                                            df.account_nm == '투자활동으로인한현금흐름') |
                                    (df.account_nm == '투자활동으로 인한 순현금흐름') | (df.account_nm == '투자활동으로인한 순현금흐름') | (
                                            df.account_nm == '2.투자활동현금흐름') |
                                    (df.account_nm == 'Ⅱ.투자활동현금흐름') | (df.account_nm == 'Ⅱ. 투자활동현금흐름') | (
                                            df.account_nm == 'II. 투자활동으로 인한 현금흐름') |
                                    (df.account_nm == 'II.투자활동으로 인한 현금흐름') | (df.account_nm == 'II. 투자활동현금흐름') |
                                    (df.account_nm == '투자활동순현금흐름 합계') | (df.account_nm == '투자활동으로부터의 순현금유입(유출)') | (
                                            df.account_nm == 'Ⅱ. 투자활동으로 인한 순현금흐름'))


def get_condition10(df):
    # 자산총계
    return (df.sj_nm == '재무상태표') & ((df.account_nm == '자산총계') | (df.account_nm == '자  산  총  계') |
                                    (df.account_nm == '자산 총계') | (df.account_nm == '자본과부채총계') |
                                    (df.account_nm == '자    산    총    계')
                                    )  # 자산총계


def get_condition11(df):
    # 매출 원가
    return ((df.sj_nm == '손익계산서') | (df.sj_nm == '포괄손익계산서')) & (df.account_nm == '매출원가')


def get_condition12(df):
    # 순이익
    return ((df.sj_nm == '손익계산서') | (df.sj_nm == '포괄손익계산서')) & (df.account_nm == '법인세비용차감전순이익(손실)')


def get_condition13(df):
    # 지출비용
    return ((df.sj_nm == '손익계산서') | (df.sj_nm == '포괄손익계산서')) & (df.account_nm == '법인세비용(혜택)')


def get_condition14(df):
    return ((df.sj_nm == '손익계산서') | (df.sj_nm == '포괄손익계산서')) & (df.account_nm == 'II.재료비')  # 008770 매출총이익 계산하기 위한 것

def get_condition15(df):
    # 유형자산의 증가
    return (df.sj_nm == '현금흐름표') & ((df.account_nm == '유형자산의 증가') | (df.account_nm == '유형자산의증가') |
                                    (df.account_nm == '　유형자산의 취득') | (df.account_nm == '　유형자산의취득') |
                                    (df.account_nm == '유형자산의취득') | (df.account_nm == '유형자산의 취득') |
                                    (df.account_nm == '유형자산 취득')
                                    )
