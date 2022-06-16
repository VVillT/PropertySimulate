# This app is for educational purpose only. Insights gained is not financial advice. Use at your own risk!
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime, csv, base64


#---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(layout="wide")
#---------------------------------#

# Get the dates for operations
#First date of the full year 4 years ago: 
startdate = (pd.Timestamp.today() - pd.DateOffset(days=1)).date()
beginningof4yearsgo = datetime.datetime(pd.to_datetime("today").year - 4 , 1, 1).date()
beginningof3yearsgo = datetime.datetime(pd.to_datetime("today").year - 3 , 1, 1).date()
beginningof2yearsgo = datetime.datetime(pd.to_datetime("today").year - 2 , 1, 1).date()
beginningoflastyear = datetime.datetime(pd.to_datetime("today").year - 1 , 1, 1).date()
beginningofthisyear = datetime.datetime(pd.to_datetime("today").year , 1, 1).date()
enddate = datetime.datetime(pd.to_datetime("today").year + 25 , 1, 1).date()
#---------------------------------#
# Page layout (continued)
## Divide page to 3 columns (col1 = sidebar, col2 and col3 = page contents)
col1 = st.sidebar
col2, col3 = st.columns((2,1))

# Sidebar + Main panel
col1.header('Input Options')
ticket_input = 50000
propertycost = col1.number_input("Enter cost of buying the property. For Example: 250k", ticket_input)
rentinput = 100
propertyrent = col1.number_input("Enter income of monthly rental income of the property. For Example: £1200pcm", rentinput)
spentinput = 100
propertymain = col1.number_input("Enter quarterly cost of repair etc. For Example: £500 per quarter", spentinput)



st.title('Property investment Basic Simulation  App')
st.markdown("""
This app predicts the return of investment on a Month-on-Month basis. 
""")
#---------------------------------#
# About
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, csv, datetime
* **Data source:** Yourself
* **Support:** Please sponsor by visiting https://www.buymeacoffee.com/thedataguy to support my app hosting if you find it useful, ideas welcome! 
""")



d = pd.date_range(start=startdate, end=enddate, freq='MS')    
df = pd.DataFrame(d)
df.columns = ['Fulldate']
df['MonthYear'] = df['Fulldate'].dt.strftime('%b-%Y')
df['InvesmentCost'] = 0
df.at[0,'InvesmentCost'] = propertycost
df['MonthlyRent'] = propertyrent
df['AccumRent'] = df['MonthlyRent'].cumsum()
df['QtrtlySpend'] = 0
df.loc[df.index % 3 == 0 , 'QtrtlySpend'] = propertymain
df['account'] = df['MonthlyRent'] - df['InvesmentCost'] - df['QtrtlySpend'] 
df['AccumAccount'] = df['account'].cumsum()

breakevendate = df.loc[df['AccumAccount'].abs().idxmin(),'MonthYear']

st.write('This property will breakeven by ', breakevendate )

plotdata = df[['AccumAccount','AccumRent']].set_index(df['Fulldate'])
st.line_chart(plotdata)

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="propertydata.csv">Download CSV File for simulation data below </a>'
    return href

st.markdown(filedownload(df), unsafe_allow_html=True)

st.dataframe(df)