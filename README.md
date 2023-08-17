# Screening inventment data using Python

파이썬과 몇몇 라이브러리를 이용하여 아래의 정보들을 추출한 뒤, 몇몇의 조건을 설정하여 스크리닝을 합니다.
- 부동산
- 주식

## requirements.txt
```
beautifulsoup4==4.10.0
certifi==2021.10.8
charset-normalizer==2.0.12
DateTime==4.4
decorator==5.1.1
Deprecated==1.2.13
et-xmlfile==1.1.0
finance-datareader==0.9.32
idna==3.3
lxml==4.8.0
numpy==1.22.3
OpenDartReader==0.1.6
openpyxl==3.0.9
pandas==1.4.1
pykrx==1.0.32
python-dateutil==2.8.2
pytz==2021.3
requests==2.27.1
requests-file==1.5.1
self==2020.12.3
six==1.16.0
soupsieve==2.3.1
tqdm==4.63.0
urllib3==1.26.9
wrapt==1.14.0
xlrd==2.0.1
zope.interface==5.4.0
pyOpenSSL==22.0.0
ndg-httpsclient==0.5.1
pyasn1==0.4.8
```

## How to use

아래 Tistory 시리즈에서 작성과정 및 사용법들을 기재하고 있습니다.

👉🏻 [뇌동매매를 막아주는 파이썬 종목 스크리닝](https://drop-by-drop-fills-the-tub.tistory.com/category/%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%9C%BC%EB%A1%9C%20%EC%A2%85%EB%AA%A9%20%EC%8A%A4%ED%81%AC%EB%A6%AC%EB%84%88%20%EB%A7%8C%EB%93%A4%EA%B8%B0)
👉🏻 [파이썬으로 부동산 매매가 조회기 만들기](https://drop-by-drop-fills-the-tub.tistory.com/category/%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%9C%BC%EB%A1%9C%20%EB%B6%80%EB%8F%99%EC%82%B0%20%EB%A7%A4%EB%A7%A4%EA%B0%80%20%EC%A1%B0%ED%9A%8C%EA%B8%B0%20%EB%A7%8C%EB%93%A4%EA%B8%B0)

### OpenDart API Key
config 아래에 `api_key.py` 를 생성하신 후, API Key의 설정이 필요합니다.
```
OPEN_DART_KEY = {YOUR_OPEN_DART_KEY}
```
키의 발급은 [OpenDart](https://opendart.fss.or.kr) 에서 발급하시면 됩니다.

### data.go API Key
config 아래에 `api_key.py` 를 생성하신 후, API Key의 설정이 필요합니다.
```
PUBLIC_DATA_PORTAL = {YOUR_PUBLIC_DATA_PORTAL}
```



### Export screening file
현재 결과물은 엑셀파일로 내보내기를 하고 있습니다만, 엑셀을 사용하지 않으시는 분들은, 생성된 파일을
구글 스프레드 시트 등에 업로드하여서 열람할 수도 있고, 저장 확장자를 `*.csv` 로 바꾸어서 편하신대로 사용할 수 있습니다.

저장 경로는 `exporter.export_to_excel_with_many_sheets()`의 첫번째 파라미터로 지정해주세요.


