# 셀레니움 자동화 실습 3
# 아파트 단지 정보에서 주차장 정보 추출
# k-apt.go.kr
# => 2022.01, 서울, 강남구, 삼성동, 삼성래미안 2차

import requests
# 우리단지 검색
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
url1 = 'http://k-apt.go.kr/cmmn/bjd/getBjdList.do'
url2 = 'http://k-apt.go.kr/kaptinfo/getKaptList.do'
url3 = 'http://k-apt.go.kr/cmmn/selectKapt.do'
url4 = 'http://www.k-apt.go.kr/kaptinfo/getKaptInfo_detail.do'


# 우리단지 검색시 시도별 코드 조회

params = {'bjd_code':'','bjd_gbn':'SIDO'} # 시도
res = requests.get(url1, headers=headers, params=params)
print(res.text)

# 우리단지 검색시 시도/ 시군구/ 동별 아파트 정보 조회

params = {'bjd_code':'11', 'bjd_gbn':'SGG'} # 시군구
res = requests.get(url1, headers=headers, params=params)
print(res.text)

params = {'bjd_code':'11680', 'bjd_gbn':'EMD'} # 읍면동
res = requests.get(url1, headers=headers, params=params)
print(res.text)

# 우리단지 검색시 시도/시군구/동별 아파트 정보 조회
params = {'bjd_code':'11680105', 'search_date':'202206'}
res = requests.get(url2, headers=headers, params=params)
print(res.text)

# 지정한 아파트 정보 조회
params = {'bjd_code':'1168010500', 'kapt_code': 'A13509003' ,'search_date':'202206', 'kapt_usedate':'','kapt_name':'','go_url':'/kaptinfo/openkaptinfo.do'}
res = requests.get(url3, headers=headers, params=params)
print(res.text)

# 지정한 아파트의 주차장정보 조회1
params = {'bjd_code':'1168010500', 'kapt_code': 'A13509003' ,'search_date':'202206', 'kapt_usedate':'','kapt_name':'','go_url':'/kaptinfo/openKaptMng.do'}
res = requests.get(url3, headers=headers, params=params)
print(res.text) # 관리시설정보 페이지에 대한  html코드만 넘어옴

# 지정한 아파트의 주차장정보 조회2
params = {'kapt_code': 'A13509009'}
res = requests.get(url4, headers=headers, params=params)
print(res.text) # PCNT확인
