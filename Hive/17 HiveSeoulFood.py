import jaydebeapi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

seoul = pd.read_csv('c:/Java/seoulfood.csv')

# 쓸모없는 컬럼이 너무 많음
seoul.head()
seoul.info()

url = 'jdbc:hive2://192.168.226.132:10000/bigdata'
drv = 'org.apache.hive.jdbc.HiveDriver'
path ='c:/Java/hive-jdbc-2.3.8-standalone.jar'

sql = 'select status, endate, clodate, cendate, reopenda, totnum, whobuilding, bozungum, wolsae from seoulfood'

conn = jaydebeapi.connect(url = url, jclassname=drv, jars=path)
seoulfood = pd.read_sql(sql, conn)
conn.close()

# 테이블은 대충 다 문자로 생성 (string)

# 월세 숫자화
seoulfood.wolsae = pd.to_numeric(seoulfood.wolsae)
seoulfood.wolsae.fillna(0, inplace=True)

# 널값을 지워줘야 numeric이 가능한듯. 안된다. 차라리 테이블을 지우고 다시 생성.
# 테이블에 int값을 넣었는데도 자꾸 string으로 생성된다. 뭐지?

seoulfood.info()

# 보증금 / 월세 평균값
# 보증금은 n이 들어가있어서 안됨
wolsae_avg = np.mean(seoulfood.wolsae)
print(wolsae_avg)
# 서울 음식점 월세의 평균값은 42.86


# 지나치게 광범위하게 잡혀서, 함수로 한번 정리해줘야 할듯?
def getwolsae(x):
    wolsae = 0
    if x==0 : wolsae = 'null'
    elif 0<=x<20 : wolsae = 'under20'
    elif 20<=x<40 : wolsae = '2040s'
    elif 40<=x<60 : wolsae = '4060s'
    elif 60<=x<80 : wolsae = '6080s'
    elif 80<=x<100 : wolsae = '80100s'
    elif 100<=x<150 : wolsae = '100150s'
    elif 150<=x<200 : wolsae = '150200s'
    else : wolsae = 'buza'
    return wolsae

seoulfood['wolsae'] = seoulfood.wolsae.apply(lambda  x : getwolsae(x))
sns.countplot(data=seoulfood, x='wolsae')
plt.show()
# 월세 그래프는 0~20 > 2040 > null > 4060 > 6080 > 80100 > 100150 > buza > 150200순으로 많았다

# 테스트파일 저장
seoulfood.to_csv('c:/Java/testsample.csv', sep=',', na_rep='NaN', index=False)
