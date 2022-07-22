# 셀레니움 자동화 실습1
# 코레일에 자동로그인한 후 열차 예매하기
# https://www.letskorail.com
# 크롬드라이버 자동 설치 관련 : pip install webdriver_manager

import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://www.letskorail.com'
userid = '1360134459'
passwd = 'cyk1302sky*'


seat = '창측좌석'
stdrt = '순방향석'
dept = '서울'
dset = '부산'
dyear = '2022'
dmonth = '7'
dday = '29'
dtime = '10 (오전10)'


# 크롬드라이버 초기화
options = webdriver.ChromeOptions()
services = Service(ChromeDriverManager().install()) # 크롬드라이버 자동설치
chrome = webdriver.Chrome(service=services, options=options)

# 브라우저 창을 최대로 키움
chrome.maximize_window()
time.sleep(2)

# 코레일 메인페이지로 이동
chrome.get(url)

# 팝업창 닫기
# 부모창에서 자식창으로 제어를 이동시킨 후 창을 닫고 다시 부모창으로 제어를 옮겨야 함
# switch_to.window 함수를 이용하면 창 사이 제어권을 이동시킬 수 있음
print(chrome.window_handles) # 현재 활성화된 창들 확인

# 자식창(팝업창)으로 제어를 넘김 후 창을 닫음
chrome.switch_to.window(chrome.window_handles[1])
chrome.close()
time.sleep(1)

# 부모창으로 제어를 다시 가져옴
chrome.switch_to.window(chrome.window_handles[0])
time.sleep(1)

# 로그인 페이지로 이동
# 셀레니움에서 특정 요소를 css선택자로 제어하려면
# find_element(By.탐색유형, 탐색값)
chrome.find_element(By.CSS_SELECTOR, 'ul.gnb_list li:nth-child(2) a').click()
time.sleep(2)



# 멤버십번호/ 비밀번호 입력
# sendkey함수를 사용

# 코레일 멤버십번호
#txtMember
# chrome.find_element(By.CSS_SELECTOR, 'ul.login_mem li:first-child input')
uid = chrome.find_element(By.ID, 'txtMember')
uid.send_keys(userid)
time.sleep(1)


#txtPwd
# chrome.find_element(By.CSS_SELECTOR, 'ul.login_mem li:nth-child(2) input')
pwd= chrome.find_element(By.ID, 'txtPwd')
pwd.send_keys(passwd)
time.sleep(1)


# 로그인 버튼 클릭

#loginDisplay1 > ul > li.btn_login > a > img
# chrome.find_element(By.CSS_SELECTOR, 'li.btn_login a').click()
# //*[@id="loginDisplay1"]/ul/li[3]/a/img
chrome.find_element(By.XPATH, "//img[@alt='확인']").click()
time.sleep(3)

# 로그인후 팝업창 닫기
chrome.switch_to.window(chrome.window_handles[1])
chrome.close()
time.sleep(1)

chrome.switch_to.window(chrome.window_handles[0])
time.sleep(1)

# 도착역을 아산으로 설정
dest = chrome.find_element(By.NAME, 'txtGoEnd')
dest.clear()
dest.send_keys('아산')

# 승차권 예매
chrome.find_element(By.XPATH, "//img[@alt='승차권예매']").click()
time.sleep(1)

# 경고창 닫기
# switch_to.alert 함수를 이용하면 경고창을 제어할 수 있음
print(chrome.switch_to.alert.accept()) # 경고창 메시지 확인
chrome.switch_to.alert.accept() # 경고창 확인 버튼 클릭

# 안내메시지 페이지에서 열차예매 페이지로 이동
chrome.find_element(By.CLASS_NAME, 'btn_blue_ang').click()
time.sleep(3)

# 열차예매정보 입력 - 좌석정보
st01 = Select(chrome.find_element(By.ID, 'seat01'))
st01.select_by_visible_text(seat)

st02 = Select(chrome.find_element(By.ID, 'seat02'))
st02.select_by_visible_text(stdrt)

time.sleep(1)




stst = '서울'
enst = '아산'
seoul= chrome.find_element(By.NAME, 'txtGoStart')
seoul.clear()
seoul.send_keys(stst)
asan = chrome.find_element(By.NAME, 'txtGoEnd')
asan.clear()
asan.send_keys(enst)

syear = Select(chrome.find_element(By.ID, 's_year'))
syear.select_by_visible_text(dyear)

smonth = Select(chrome.find_element(By.ID, 's_month'))
smonth.select_by_visible_text(dmonth)

sday = Select(chrome.find_element(By.ID, 's_day'))
sday.select_by_visible_text(dday)

shour = Select(chrome.find_element(By.ID, 's_hour'))
shour.select_by_visible_text(dtime)

# ktx/srt 선택

chrome.find_element(By.XPATH, "//input[@title='전체']").click() # 아산에는 ktx가 없나보다..
# chrome.find_element(By.ID, 'selGoTrainRa00').click()

# 조회하기
chrome.find_element(By.CLASS_NAME, 'btn_inq').click()
time.sleep(1)

# 조회하면 아래로 스크롤
# 브라우저의 특정 액션은 자바스크립트 코드를 이용해서 처리
# chrome.execute_script(실행할 코드)
chrome.execute_script('window.scrollTo(0, 1000);')
time.sleep(1)


# 승차권 예매버튼
# 서울-아산은 환승만있어서 2개버튼 눌러야 예약 가능함
chrome.find_element(By.NAME, 'btnRsv1_0').click()
time.sleep(1)
chrome.find_element(By.NAME, 'btnRsv1_1').click()
time.sleep(1)


# 예약하기
# chrome.find_element(By.NAME, 'btnRsv2_8').click()


# 크롬드라이버 종료
# chrome.close()
