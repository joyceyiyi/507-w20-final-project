import plotly.plotly as py
import sqlite3
import pandas as pd

conn = sqlite3.connect('crime.db')
cursor = conn.cursor()
query = "SELECT Month, Count(Id) FROM Crimes GROUP BY Month"
cursor.execute(query)

rows = cursor.fetchall()

df = pd.DataFrame([[ij for ij in i] for i in rows])
df.rename(columns={0:"Month",1:"Frequency"})
df = df.sort_values(['Month'],ascending=[1])