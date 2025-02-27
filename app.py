import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.rcParams['font.family'] = 'Meiryo'
from matplotlib import font_manager
from datetime import datetime


font_path = "NotoSansJP-Regular.ttf"
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'Noto Sans JP'
plt.rcParams['axes.unicode_minus'] = False


st.set_page_config(page_title="東京でのワクチン接種数", layout="wide")
st.title("東京でのワクチン接種数")


df = pd.read_csv("02_tokyo_daily_vaccines.csv", encoding='utf-8-sig')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')
df['Cumulative_Vaccinations'] = df['Vaccinations'].cumsum()


date_min = df['date'].min()
date_max = df['date'].max()

start_date, end_date = st.sidebar.date_input(
    "日付範囲を選択:",
    [date_min, date_max],
    min_value=date_min,
    max_value=date_max
)

filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

st.subheader("日別接種数の推移")
fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.bar(filtered_df['date'], filtered_df['Vaccinations'], color='#4c72b0', label='日別接種数')
ax1.set_xlabel("日付")
ax1.set_ylabel("接種数")
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
plt.xticks(rotation=45)
ax1.legend()
st.pyplot(fig1)


st.subheader("累計接種数の推移")
fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.plot(filtered_df['date'], filtered_df['Cumulative_Vaccinations'], color='#55a868', linewidth=2)
ax2.set_xlabel("日付")
ax2.set_ylabel("累計接種数")
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
plt.xticks(rotation=45)
st.pyplot(fig2)


