import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv('startups_cleaned.csv')
st.set_page_config(layout="wide",page_title='StartUp Analysis')


def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investment of the investor
    last_5_df = df[df['investor'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount_in_inr']]
    st.subheader('Most Recent Investment')
    st.dataframe(last_5_df)

    col1 , col2 = st.columns(2)
    with col1:
        # biggest investment
        big_series = df[df['investor'].str.contains(investor)].groupby('startup')['amount_in_inr'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig,ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investor'].str.contains(investor)].groupby('vertical')['amount_in_inr'].sum()
        st.subheader('Sectoral Investment')
        fig1,ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct='%1.1f%%')
        st.pyplot(fig1)
    df['date'] = df['date'].str.replace('05/072018', '05/07/2018')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['year'] = df['date'].dt.year

    year_series = df[df['investor'].str.contains(investor)].groupby('year')['amount_in_inr'].sum()
    st.subheader('YoY Investment')

    fig2,ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)
    st.pyplot(fig2)




st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'StartUp', 'Investor'])
if option == 'Overall Analysis':
    st.title('Overall Analysis')
elif option == 'StartUp':
    st.sidebar.selectbox('Select StartUp', sorted(df['startup'].unique().tolist()))
    st.title('StartUp Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investor'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
