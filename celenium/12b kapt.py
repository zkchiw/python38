# 아파트 단지 정보에서 주차장 정보 추출
# k-apt.go.kr
# 메인페이지 팝업창 닫기 => '단지정보' 클릭
# => 2022.01, 서울, 강남구, 삼성동, 아이파크삼성동 클릭


import time

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'http://www.k-apt.go.kr/'

options = webdriver.ChromeOptions()
services = Service(ChromeDriverManager().install()) # 크롬드라이버 자동설치
chrome = webdriver.Chrome(service=services, options=options)

chrome.maximize_window()
chrome.get(url)
time.sleep(2)

# 팝업창 닫기

# 1)필독 안내사항
chrome.find_elements(By.CLASS_NAME, 'layerP_close')[0].click()
# chrome.find_element(By.CLASS_NAME, 'layerP_close').click()
time.sleep(1)
# 2)자주하는질문
chrome.find_elements(By.CLASS_NAME, 'layerP_close')[1].click()
# chrome.find_element(By.CSS_SELECTOR, '#layerPopup202204221 div button i').click()
time.sleep(1)

# 자바스크립트를 이용한 방법
# chrome.execute_script('closePopupLayer("#layerPopup20211208")')
# time.sleep(2)
# chrome.execute_script('closePopupLayer("#layerPopup202204221")')
# time.sleep(2)

# 단지정보 들어가기 1
chrome.find_element(By.XPATH, "//a[@title='단지정보']").click()
time.sleep(2)
# 단지정보 들어가기 2
chrome.find_element(By.XPATH, "//a[@title='우리단지 기본정보']").click()
time.sleep(3)

## 단지정보 입력

# 년도, 월 입력
# //*[@id="bjdGroup"]/div/div/dl[1]/dd/div/select[1]/option[1] 2022년도
chrome.find_element(By.XPATH, '//*[@id="bjdGroup"]/div/div/dl[1]/dd/div/select[1]/option[1]').click()

year = Select(chrome.find_element(By.NAME, 'searchYYYY'))
year.select_by_visible_text('2022년')
time.sleep(1)

# //*[@id="bjdGroup"]/div/div/dl[1]/dd/div/select[2]/option[6] 6월
chrome.find_element(By.XPATH, '//*[@id="bjdGroup"]/div/div/dl[1]/dd/div/select[2]/option[6]').click()

month = Select(chrome.find_element(By.NAME, 'searchMM'))
month.select_by_visible_text('06월')
time.sleep(1)

# 광역시, 시군구
# //*[@id="bjdGroup"]/div/div/dl[2]/dd/select/option[2] 서울시
# //*[@id="bjdGroup"]/div/div/dl[2]/dd/div/select[1]/option[2] 강남구
# //*[@id="bjdGroup"]/div/div/dl[2]/dd/div/select[2]/option[6] 삼성동


# 따로따로 구역을 잡아주면서 실행하면 아무 이상없이 끝까지 잘 돌아가지만, 자동실행시키면 중간에 멈춘다?
# 중간중간 timesleep를 줘보면 되나

chrome.find_element(By.XPATH, '//*[@id="bjdGroup"]/div/div/dl[2]/dd/select/option[2]').click()
time.sleep(2)
chrome.find_element(By.XPATH, '//*[@id="bjdGroup"]/div/div/dl[2]/dd/div/select[1]/option[2]').click()
time.sleep(2)
chrome.find_element(By.XPATH, '//*[@id="bjdGroup"]/div/div/dl[2]/dd/div/select[2]/option[6]').click()
time.sleep(2)


# # 스크롤을 아래로 내리지 않으면 래미안 라클라시가 나옴
# 아파트 결과 목록 출력 2
html = BeautifulSoup(chrome.page_source, 'lxml')
for apt in html.select('p.aptS_rLName'):
    print(apt.text)

# 클릭대상 요소의 선택자 : #mCSB_2_container ul li:nth-child(???) a
# 결과 목록에서 '삼성래미안2차'의 위치(index)를 파악

idx = 1
for j in html.select('p.aptS_rLName') :
    if j.text =='아이파크삼성동':break
    else : idx=idx+1
print(idx) # 아이파크삼성동 16번째

# 결과 목록 각 항목 높이 알아내기
elm = chrome.find_element(By.CSS_SELECTOR, '#mCSB_2_container ul li:nth-child(1)')
print(elm.size['height'])


# 자동 스크롤 기능 구현
# 결과목록 각 항목 높이 : 대충 70px
# 현재 화면에 출력된 결과 목록 수 : 7개
# 아이파크삼성동의 인덱스 : 16
elm = chrome.find_element(By.CSS_SELECTOR, '#mCSB_2_container')
# 스크롤하면 스타일의 top값이 바뀜 (0~-478)
# 셀레니움을 이용해서 스타일을 제어 가능
# pos = '-600px'
pos ='-'+str(int((idx-7) * 70)) + 'px'
chrome.execute_script(f'arguments[0].style="position:relative; top:{pos}; left:0;"',elm)
time.sleep(2)

# 스크롤을 끝까지 내리지 않으면 오류나서 실행되지 않음
ipark = f'#mCSB_2_container ul li:nth-child({idx}) a'
chrome.find_element(By.CSS_SELECTOR, ipark).click()
time.sleep(4)


# 아파트 기본정보 출력 (아파트 정보 조회에 들어가서)
aptname = chrome.find_element(By.CSS_SELECTOR, 'table.contTbl tbody tr:nth-child(1) td:nth-child(2)')
print(aptname.text)

# 아파트 주소 출력
aptaddr = chrome.find_element(By.CSS_SELECTOR, 'table.contTbl tbody tr:nth-child(2) td:nth-child(2)')
print(aptaddr.text)

# 아파트 관리정보 출력(주차대수)

# 관리시설정보에 들어감
chrome.find_element(By.XPATH, '//*[@id="container"]/div[2]/div[1]/ul/li[3]' ).click()
time.sleep(1)

# 지상 주차대수
jsjc = chrome.find_element(By.ID, 'kaptd_pcnt').text
print(f'지상 주차가능 차량은 {jsjc}대')

# 지하 주차대수
jhjc = chrome.find_element(By.ID, 'kaptd_pcntu').text
print(f'지하 주차가능 차량은{jhjc}대')

# 총 주차대수
totjc = chrome.find_element(By.ID, 'kaptd_total_pcnt').text
print(f'총 주차가능 차량은{totjc}대')


# 그리고 할거 다하면 왜 꺼지는건지 모르겠네? close도 안넣어놨는데

# 크롬 드라이버 종료
chrome.close()