
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="미국 대형주 수익률 비교", layout="wide")
st.markdown("""
    <style>
    .dataframe td, .dataframe th {
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)
st.title("📊 미국 시가총액 TOP 10 기업 수익률 비교 대시보드")

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B', 'AVGO', 'LLY']

@st.cache_data
def get_price_data(tickers):
    end = datetime.today()
    start = end - timedelta(days=5*365)
    data = yf.download(tickers, start=start, end=end, auto_adjust=True)['Close']
    return data

def calculate_returns(df, periods):
    returns = {}
    for label, days in periods.items():
        ret = df.pct_change(periods=days).iloc[-1]
        returns[label] = (ret * 100).round(2)
    return pd.DataFrame(returns)

periods = {
    '1일': 1,
    '1주일': 5,
    '1개월': 21,
    '6개월': 126,
    '1년': 252,
    '3년': 756,
    '5년': 1260,
}

with st.spinner("데이터를 불러오는 중입니다..."):
    df = get_price_data(tickers)
    return_df = calculate_returns(df, periods)

st.markdown("### 📈 수익률 (%)", unsafe_allow_html=True)
st.dataframe(return_df.style.format("{:.2f}"), use_container_width=True)

selected = st.selectbox("📌 종목별 주가 추이 보기", tickers)
if selected:
    st.line_chart(df[selected])
