import streamlit as st #pip install streamlit
import pandas as pd    #pip install pandas
import numpy as np     #pip install numpy

#create a method to filter the data, return filtered dataframe, the argument is the pd datafram 
#reference: https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/
def dynamicFilter(loaded_df):
    #placed at sidebar, and define the subheader, and created a sentinel as onFilter to turn on the filter function 
    st.sidebar.subheader('Filter Settings')
    onFilter = st.sidebar.checkbox("Add filters")

    if not onFilter:
        return loaded_df

    loaded_df = loaded_df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in loaded_df.columns:
        if pd.api.types.is_object_dtype(loaded_df[col]):
            try:
                loaded_df[col] = pd.to_datetime(loaded_df[col])
            except Exception:
                pass

        if pd.api.types.is_datetime64_any_dtype(loaded_df[col]):
            loaded_df[col] = loaded_df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.sidebar.multiselect("Filter dataframe on", loaded_df.columns)
        for column in to_filter_columns:
            #define the column width
            left,right = st.columns((1,20))
            # Treat columns with < 10 unique values as categorical
            if pd.api.types.is_categorical_dtype(loaded_df[column]) or loaded_df[column].nunique() <10:
                #display at main part(on the right of the screen)
                left.write("-")
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    loaded_df[column].unique(),
                    default=list(loaded_df[column].unique()),
                )
                loaded_df = loaded_df[loaded_df[column].isin(user_cat_input)]
            elif pd.api.types.is_numeric_dtype(loaded_df[column]):
                _min = float(loaded_df[column].min())
                _max = float(loaded_df[column].max())
                step = (_max - _min) / 100
                #only the numeric factors show at side bar (on left of the screen)
                user_num_input = st.sidebar.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                loaded_df = loaded_df[loaded_df[column].between(*user_num_input)]
            elif pd.api.types.is_datetime64_any_dtype(loaded_df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        loaded_df[column].min(),
                        loaded_df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    loaded_df = loaded_df.loc[loaded_df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    loaded_df = loaded_df[loaded_df[column].astype(str).str.contains(user_text_input)]

    return loaded_df