# hive에서 titanic 데이터셋을 불러온 뒤 간단한 탐색적 분석 실시

import jaydebeapi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# 접속주소/hive-jdbc 드라이버 지정
url = 'jdbc:hive2://192.168.226.132:10000/bigdata'
drv = 'org.apache.hive.jdbc.HiveDriver'

# 사용할 hive-jdbc 드라이버  위치 지정
path ='c:/Java/hive-jdbc-2.3.8-standalone.jar'

# pandas 출력 설정
pd.set_option('display.expand_frame_repr', False)

# 불러올 데이터셋 지정
sql = 'select * from titanic'

# hive로부터 타이타닉 데이터 읽어오기 1
conn = jaydebeapi.connect(url = url, jclassname=drv, jars=path)
titanic = pd.read_sql(sql, conn)
conn.close()

# hive로부터 타이타닉 데이터 읽어오기 2
# pd.read_csv(파일명, 구분자, 인코딩)
titanic2 = pd.read_csv('c:/Java/titanic.csv')

# 데이터 확인
# head(행수), tail(행수)
titanic.head()
titanic2.head()
titanic2.tail()

# 데이터 구조 확인 : 데이터 유형, 총 갯수, 결측치 여부
# info
titanic.info
titanic2.info()

# 데이터프레임 컬럼명 변경
# 객체명.columns = [값1, 값2 , 값3, .... ]

titanic.columns = ['pclass','survived','name','sex', 'age','sibsp','parch','ticket','fare', 'cabin','embarked']
titanic.tail(10)

# 빈 문자열을 null로 바꾸기 (결측치)
# replace(찾을 값, 바꿀 값, regex=True)
titanic.replace('', np.nan, regex=True)

# 메모리에 저장된 것을 타이타닉 테이블에도 적용
titanic = titanic.replace('', np.nan, regex=True)
titanic.tail(10)

titanic.info

# 컬럼에 대한 데이터형식을 적절히 변환
# 컬럼 지정 : 객체명.컬럼명, 객체명['컬럼명']
# 숫자형 변환 : pd.to_numeric(컬럼명)
# 또다른 변환 : 객체명.astype({컬럼명:자료형, ...})

titanic.pclass
titanic.pclass.head()

titanic.pclass = pd.to_numeric(titanic.pclass)

# survived, age, sibsp, parch, fare 숫자형태로 변환
titanic.survived = pd.to_numeric(titanic.survived)
titanic.age = pd.to_numeric(titanic.age)
titanic.sibsp = pd.to_numeric(titanic.sibsp)
titanic.parch = pd.to_numeric(titanic.parch)
titanic.fare = pd.to_numeric(titanic.fare)
titanic.info()

titanic.astype({'pclass':int}) # null값이 있어서 변환 불가

# 결측치(missing value) 처리
# 처리방법 : 삭제, 대체값
# age : 전체 1310개 중에 1046개만 온전한 데이터 -> 대체값 넣기
# cabin : 전체 1310개 중에 295개만 온전한 데이터 -> 컬럼 삭제
titanic.describe()

# 승객의  평균 나이 계산 : np.mean
age_mean = np.mean(titanic.age)
print(age_mean)

# 결측치 대체값 넣기
# 컬럼명.fillna(대체값, inplace = True)
titanic.age.fillna(age_mean, inplace=True)

# 컬럼 삭제하기
# drop(대상컬럼, axis=1) # 삭제방향은 컬럼(열-세로)
titanic.drop(['cabin'], axis=1, inplace=True)

# 결측치가 포함된 행을 모두 정리(삭제)
# 객체명.dropna()
titanic.dropna(inplace=True)

# dataq.or.kr


# 탐색적 분석 1
# pclass : 승객/좌석 등급
# survived : 승객 생존여부
# sex : 승객 성별
# embarked : 승객 승선항구

# 분석방법 - 빈도계산 - value_counts
titanic.pclass.value_counts()
titanic.survived.value_counts() # 0 사망 1 생존
titanic.sex.value_counts()
titanic.embarked.value_counts()

# 관심대상 변수 시각화 - 막대그래프
# 대상컬럼.value_counts().plot.bar()

titanic.pclass.value_counts().plot.bar()
titanic.survived.value_counts().plot.bar()
titanic.sex.value_counts().plot.bar()
titanic.embarked.value_counts().plot.bar()

titanic.age.value_counts().plot.hist()
plt.show()

# 범주형 데이터를 문자열로 변환
# 파생변수 : life, seat, ports
# dead/live, 1st/2st/3st, cherbourg/queenstown/southampthon

def getlife(x): # 생존여부를 문자로 변환해서 출력
    life = 'dead'
    if x ==1. : life = 'live'
    return life

def getseat(x):
   seat = '1st'
   if x ==2: seat = '2nd'
   elif x ==3 : seat = '3rd'
   return seat

def getport(x):
    port = 'cherbourg'
    if x == 'S': port = 'southampthon'
    elif x =='Q' : port = 'queenstown'
    return port


# 정의한 함수를 컬럼의 각 행에 적용
# 객체명[파생컬럼명] = 컬럼명.apply(lambda x:함수명)
titanic['life'] = titanic.survived.apply(lambda  x : getlife(x))
titanic.head()

# 관심대상 변수 시각화 - 막대그래프
# sns.countplot(data=객체명, x= 변수명)
sns.countplot(data=titanic, x='life')
plt.show()

titanic['seat'] = titanic.pclass.apply(lambda  x : getseat(x))
sns.countplot(data=titanic, x='seat')
plt.show()

titanic['port'] = titanic.embarked.apply(lambda  x : getport(x))
sns.countplot(data=titanic, x='port')
plt.show()

# 승객의 나이를 시각화
# 연속형 데이터를 범주형으로 변환한 후 막대그래프로 시각화

# ~1 : 신생아 sin/ ~5 : 유아 yua/ ~10 : 청소년 chun/ 11~19 : 10대 10s/ 20대, 30대, 40대 ....

def getage(x):
    age = 0
    if x<1 : age = 'sin'
    elif 1<=x<5 : age = 'yua'
    elif 5<=x<10 : age = 'chun'
    elif 10<=x<20 : age = '10s'
    elif 20<=x<30 : age = '20s'
    elif 30<=x<40 : age = '30s'
    elif 40<=x<50 : age = '40s'
    elif 50<=x<60 : age = '50s'
    elif 60<=x<70 : age = '60s'

    else : age = 'teltak'
    return age

# 오류! 함수가 잘못됐나
titanic['age'] = titanic.age.apply(lambda  x : getage(x))
sns.countplot(data=titanic, x='age')
plt.show()


# 탐색적 분석 2
# 관심대상 변수 시각화2
# groupby([조건들])[대상컬럼].count()
# 승객 성별 생존 여부
titanic.groupby(['life'])['life'].count()
titanic.groupby(['sex','life'])['life'].count()
titanic.groupby(['sex','life'])['life'].count().plot.bar()
titanic.groupby(['sex','life'])['life'].count().unstack().plot.bar()
# unstack함수를 사용해서 성별별로 묶어줌
plt.show()

# 좌석 등급별 생존 여부
titanic.groupby(['seat','life'])['life'].count()
titanic.groupby(['seat','life'])['life'].count().unstack().plot.bar()
plt.show()

# 승선 항구별 생존 여부
titanic.groupby(['port','life'])['life'].count()
titanic.groupby(['port','life'])['life'].count().unstack().plot.bar()
plt.show()


# 작업한 결과물을 csv로 저장
# 객체명.to_csv (파일경로, 옵션)
# sep : 컬럼 구분자 지정
# na_rep : null값 표시 여부
# index : 각 행에 순번 지정 여부
titanic.to_csv('c:/Java/titanic2.csv', sep=',', na_rep='NaN', index=False)



# 데이터 리터러시를 키우자! : 시야를 넓히자

# - 데이터 리터러시는 데이터를 건전한 목적과 윤리적인 방법으로 사용한다는 전제 하에, 현실 세상의 문제에 대한 끊임없는 탐구를 통해 질문하고 답하는 능력
# - 좋은 질문을 할 수 있는 역량
# - 필요한 데이터를 선별하고 검증할 수 있는 역량
# - 데이터 해석 능력을 기반으로 유의미한 결론을 만들어내는 역량
# - 가설 기반 A/B 테스트를 수행하여 결과를 판별할 수 있는 역량
# - 의사결정자들도 이해하기 쉽게 분석 결과를 표현할 수 있는 역량
# - 데이터 스토리텔링을 통해 의사결정자들이 전체그림을 이해하고 분석 결과에 따라 실행하게 하는 역량















