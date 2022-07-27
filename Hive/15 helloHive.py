# 파이썬 + 하이브 연동

import jaydebeapi
import pandas as pd

# 접속주소/hive-jdbc 드라이버 지정
url = 'jdbc:hive2://192.168.226.132:10000/bigdata'
drv = 'org.apache.hive.jdbc.HiveDriver'

# 사용할 hive-jdbc 드라이버  위치 지정
path ='c:/Java/hive-jdbc-2.3.8-standalone.jar'

# sql문 정의

sql = 'select * from emp'

# python - hive 연결

conn = jaydebeapi.connect(url = url, jclassname=drv, jars=path)
cursor = conn.cursor()
cursor.execute(sql)
result = cursor.fetchall()
cursor.close()
conn.close()

# 결과 출력
print(result)

# hive에서 pandas 형식으로 데이터 불러오기
# pd.read_sql(질의문, 연결객체)
conn = jaydebeapi.connect(url = url, jclassname=drv, jars=path)
emp = pd.read_sql(sql, conn)
conn.close()

print(emp.head())
print(emp.describe())