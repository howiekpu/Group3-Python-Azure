import streamlit as st #pip install streamlit
import pandas as pd    #pip install pandas
import numpy as np     #pip install numpy

import streamlit_app as default_filter
import dynamic_filter as dynamic_filter

# show app header,title
st.subheader('INFO 4330 Group 3 Python Streamlit App Deploying by Azure web service')
st.write("Multi Columns Streamlit filter ")

#define global variable df 
global loaded_df

#Creating a method to upload the csv file, return df as pd dataframe
def uploader_csv():
    st.header("Choose a dataset")
    option = st.selectbox("Select an option:", ("Upload a CSV file", "Use YouTube Statistics"))
    
    # two options provided
    if option == "Upload a CSV file":
        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")

    elif option == "Use YouTube Statistics":
        data_path = 'data/Global_YouTube_Statistics.csv'
        df = pd.read_csv(data_path)
        st.success("Loaded YouTube Statistics dataset!")
    return df

#try to catch the dataset, if it is exist, run uploading and filter
try:
    #user uploads csv file
    loaded_df = uploader_csv()
    if loaded_df is not None:
         st.dataframe(dynamic_filter.dynamicFilter(loaded_df))
         default_filter.filter(loaded_df)
except Exception:
    #if user doesn't uploads csv file, app can show the YouTube statistic dataset by default  
    print('please choose the csv file to upload for web app')



