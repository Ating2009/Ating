import pandas as pd
from sqlalchemy import create_engine

df = pd.read_excel('蔡徐坤篮球.xlsx')

# 当engine连接的时候我们就插入数据
engine = create_engine('mysql+pymysql://root:31415926@localhost:3306/text?charset=utf8')
with engine.connect() as conn, conn.begin():
    df.to_sql('蔡徐坤篮球', conn, if_exists='replace')