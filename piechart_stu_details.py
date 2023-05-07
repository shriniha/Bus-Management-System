import streamlit as st
import os
import matplotlib.pyplot as plt
from deta import Deta

Deta_key_st="d0jxfrvb_xccodCHMbedEGgEbPjPqVHbGumk4waaF"

#initialize with project key

Deta_st=Deta(Deta_key_st)

#connect a database

stdb=Deta_st.Base("st_db")

def insert_user(total,first_yr,sec_yr,third_yr,fourth_yr):
    return stdb.put({"key":total,"first yr":first_yr,"second yr":sec_yr,"third yr":third_yr,"fourth yr":fourth_yr})
insert_user("0","0","0","0","0")

def fetch_all_st():
    stu=stdb.fetch()
    return stu.items

st_num=fetch_all_st()
st_dict=st_num[1]
first_yr=st_dict["first yr"]
sec_yr=st_dict["second yr"]
third_yr=st_dict["third yr"]
fourth_yr=st_dict["fourth yr"]





# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'First yr', 'Second yr', 'Third yr', 'Fourth yr'
sizes = [first_yr,sec_yr,third_yr,fourth_yr]
explode = (0, 0, 0, 0)  # only "explode" 
print(sizes)
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig1)





