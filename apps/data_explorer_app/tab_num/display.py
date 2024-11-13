import streamlit as st
from tab_num.logics import NumericColumn  # Import the NumericColumn class

def display_tab_num_content(df):
    # Ensure num_column is an instance of NumericColumn and initialized with the DataFrame
    if "num_column" not in st.session_state or st.session_state.num_column is None:
        st.session_state.num_column = NumericColumn(df=df)

    # Set up the numeric column instance to find and use a specific numeric column
    num_column = st.session_state.num_column

    # Find all numeric columns
    num_column.find_num_cols()

    # Dropdown to select a numeric column for exploration
    selected_column = st.selectbox("Select a numeric column to explore", num_column.cols_list)

    # Set data for the selected column and calculate relevant statistics
    num_column.set_data(selected_column)

    # Display Numeric Column Summary
    st.subheader("Numeric Column Summary")
    summary_df = num_column.get_summary()
    st.table(summary_df)  # Display the summary as a static table

    # Display Histogram
    st.subheader("Histogram")
    st.altair_chart(num_column.histogram, use_container_width=True)  # Display the histogram chart

    # Display Most Frequent Values
    st.subheader("Most Frequent Values")
    st.dataframe(num_column.frequent)  # Display the most frequent values as an interactive table
