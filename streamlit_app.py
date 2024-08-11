import streamlit as st
import pandas as pd
import plotly.express as px
# Function to load the preloaded dataset




def filter(loaded_df):
    # Title of the Streamlit app
    st.title('Dashboard for Data Analysis')

    # Initialize an empty DataFrame
    df = pd.DataFrame(loaded_df)
   
    
    # If DataFrame is not empty, display the data and visualizations
    if not df.empty:

        
        # Display basic statistics
        st.header('Basic Statistics')
        st.write(df.describe())

        
        st.header('Lets View the Best or Worst Performers')
        st.sidebar.header('Top/Bottom Performers')
        top_bottom = st.sidebar.selectbox('Select Top or Bottom', ['Top', 'Bottom'])
        top_n = st.sidebar.slider('Select number for range', min_value=1, max_value=50, value=10)
        x_axis_column = st.sidebar.selectbox('Select column for x-axis (string fields)', df.select_dtypes(include=['object']).columns, index=None)
        y_axis_column = st.sidebar.selectbox('Select column for y-axis (numeric fields)', df.select_dtypes(include=['number']).columns,index=None)

        if top_bottom == 'Top':
            youtubers = df.nlargest(top_n, y_axis_column)
        else:
            youtubers = df.nsmallest(top_n, y_axis_column)

        fig = px.bar(youtubers, x=x_axis_column, y=y_axis_column, title=f'{top_bottom} {top_n} by {y_axis_column}')
        st.plotly_chart(fig)

        categoricalCol= df.select_dtypes(include=['object']).columns
        create_rank_Bar = st.selectbox('Would you like to rank your data?', ['No','Yes'])
        if create_rank_Bar == 'Yes':
            st.header('Lets create Rank Chart')
            st.subheader('select the column you want to rank by in the sidebar')
            st.sidebar.header('Rank Chart')

                # Option to use existing rank column or create a new rank
            use_existing_rank = st.sidebar.checkbox('My dataset has Rank colunm', value=True)
            
            if not use_existing_rank:
                rank_column = st.sidebar.selectbox('Select column to generate rank by', df.columns,index=None)
                
                if df[rank_column].dtype == 'object':
                    category_counts = df[rank_column].value_counts()
                    df['rank'] = df[rank_column].map(category_counts.rank(ascending=False, method='min'))
                else:
                    df['rank'] = df[rank_column].rank(method='min', ascending=False)

            # Slider to filter by rank
            min_rank = int(df['rank'].min())
            max_rank = int(df['rank'].max())
            rank_range = st.sidebar.slider('Select rank range', min_rank, max_rank, (min_rank, max_rank))
            
            rank_df = df[(df['rank'] >= rank_range[0]) & (df['rank'] <= rank_range[1])]
            
            rank_data_column = st.selectbox('Select column you want to display with rank', categoricalCol,index=None) 

            if use_existing_rank:
                rank_chart_df = rank_df[[rank_data_column, 'rank']].set_index(rank_data_column)
            else:
                rank_chart_df = rank_df[[rank_data_column, 'rank']].set_index(rank_data_column)
            
            st.bar_chart(rank_chart_df)

    
        
        create_Line_Bar = st.selectbox('Would you like to Create line chart to display analysis over time?', ['No','Yes'])
        if create_Line_Bar == 'Yes':
            time_column = st.selectbox('Select Time colunm', df.columns,index=None)
            
            data_column = st.selectbox('Select colunm you want to display over time', df.columns,index=None)
            

            # Ensure the time column is numeric
            df[time_column] = pd.to_numeric(df[time_column], errors='coerce')
            df = df.dropna(subset=[time_column])
            df = df.sort_values(by=time_column)
            st.sidebar.header('Line Chart')
    
            # Sidebar selection for year range
            min_year = int(df[time_column].min())
            max_year = int(df[time_column].max())
            year_range = st.sidebar.slider('Select range', min_year, max_year, (min_year, max_year))

            # Filter the dataframe by the selected year range
            line_df = df[(df[time_column] >= year_range[0]) & (df[time_column] <= year_range[1])]

            # Check if the data column is numeric or not
            if pd.api.types.is_numeric_dtype(line_df[data_column]):
                # Sum the values if the data column is numeric
                time_series = line_df.groupby(time_column)[data_column].sum().reset_index()
            else:
                # Count the occurrences if the data column is not numeric
                time_series = line_df.groupby(time_column)[data_column].count().reset_index()

            # Create the line chart
            st.line_chart(time_series.set_index(time_column)[data_column])


        
        create_pie_chart = st.selectbox('Would you like to create a pie chart?', ['No', 'Yes'])
        if create_pie_chart == 'Yes':
            
            numericalCol= df.select_dtypes(include=['float64']).columns
            category_column = st.selectbox('Select category column for pie chart',categoricalCol,index=None)
            value_column = st.selectbox('Select value column for pie chart', numericalCol,index=None)
            # Sidebar selection for categories to include in the pie chart
            st.sidebar.header('Pie Chart')
            unique_categories = df[category_column].unique()
            selected_categories_for_pie = st.sidebar.multiselect('Select categories to include in pie chart', unique_categories, unique_categories)
            
            # Filter the dataframe by the selected categories
            pie_data = df[df[category_column].isin(selected_categories_for_pie)]
            
            # Aggregate the data for the pie chart
            pie_data = pie_data.groupby(category_column)[value_column].sum().reset_index()

            # Create the pie chart
            fig = px.pie(pie_data, names=category_column, values=value_column, title=f'Pie chart of {value_column} by {category_column}')
            st.plotly_chart(fig)
        create_bar_chart = st.selectbox('Would you like to create a bar chart?', ['No', 'Yes'])
        if create_bar_chart == 'Yes':

            categoricalCol= df.select_dtypes(include=['object']).columns
            numericalCol= df.select_dtypes(include=['float64']).columns
            category_column = st.selectbox('Select category column for bar chart', categoricalCol,index=None)
            value_column = st.selectbox('Select value column for bar chart', numericalCol,index=None)

            # Sidebar selection for categories to include in the bar chart
            unique_categories = df[category_column].unique()
            selected_categories_for_bar = st.sidebar.multiselect('Select categories to include in bar chart', unique_categories, unique_categories)
            
            # Filter the dataframe by the selected categories
            bar_data = df[df[category_column].isin(selected_categories_for_bar)]
            
            # Aggregate the data for the bar chart
            bar_data = bar_data.groupby(category_column)[value_column].sum().reset_index()

            # Create the bar chart
            fig = px.bar(bar_data, x=category_column, y=value_column, title=f'Bar chart of {value_column} by {category_column}')
            st.plotly_chart(fig)
        
