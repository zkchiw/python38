# selenium으로 스크레핑 하기
# 웹브라우저를 이용한 작업들을
# 자동화할 수 있도록 특수제작된 브라우저
# 또한, ajax를 이용한 동적 웹페이지를 크롤링하는데에도 사용

# seleniumhq.org
# chromedriver.chromium.org
# ChromeDriver 98.0.4758.102 (2022-02-17)
# chromedriver_win32.zip => chromedriver.exe
# C:\Program Files\Google\Chrome\Application

# pip install selenium => selenium-4.3.0 (2022-07-21)

# requests, bs4로 스크래핑할 수 없는
# 동적 데이터를 포함하는 웹 페이지를
# 원격 조작이 가능한 웹브라우저를 이용해서 처리
import htmls as htmls
from selenium import webdriver
from bs4 import BeautifulSoup
import time

url = 'https://movie.daum.net/main'

# 크롬 드라이버 실행
# 드라이버 : 셀레니움에 의해 자동화 작업이 가능하도록 특수 제작된 브라우저
chrome = webdriver.Chrome(r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')

# 지정한 url로 접속
chrome.get(url)
time.sleep(3)

# 브라우저내 메모리에 저장된 웹 소스를 bs4로 파싱(parsing)
html = BeautifulSoup(chrome.page_source, 'lxml')

# 크롬 드라이버 종료
chrome.close()

# bs4로 파싱한 웹 소스를 화면에 출력
print(html)


# 동적 웹페이지 크롤링 (다음 영화)

for title in html.select('strong.tit_item a'):
    print(title.text)

for rate in html.select('span.txt_append span:nth-child(1)'):
    print(rate.text)

for resrv in html.select('span.txt_append span:nth-child(3)'):
    print(resrv.text)

