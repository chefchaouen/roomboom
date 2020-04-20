import pymysql
import pandas as pd
import plotly
plotly.tools.set_credentials_file(username='skyline23', api_key='UBAAOuLVkNH8OYgE3pDW')
import plotly.plotly as py
from plotly.graph_objs import *

db = pymysql.connect(host="localhost", user="root", passwd="yip", db="suumo", charset="utf8")
c = db.cursor()

c.execute('SELECT rent + other_monthly_fees, floor_area, room_age, station FROM listings_2017_01_31;')
rows = c.fetchall()

df = pd.DataFrame([[ij for ij in i] for i in rows])
df.rename(columns={0:'rent and other monthly fees', 1:'floor_area', 2:'room_age', 3:'station'}, inplace=True);
df = df.sort_values(by='rent and other monthly fees', ascending=[1]);

trace1 = Scatter(
        x=df['floor_area'],
        y=df['rent and other monthly fees'],
        mode='markers'
)
layout = Layout(
        xaxis=XAxis( title = 'floor_area' ),
        yaxis=YAxis( type='log', title='rent' )
)
data = Data([trace1])
fig = Figure(data=data, layout=layout)
py.iplot(fig, filename="rent vs floor_area")

