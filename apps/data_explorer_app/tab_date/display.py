import streamlit as st

from tab_date.logics import DateColumn

def display_tab_date_content(file_path=None, df=None):
    """
    --------------------
    Description
    --------------------
    -> display_tab_date_content (function): 
        Function that will instantiate tab_date.logics.DateColumn class, save it into Streamlit session state and call its tab_date.logics.DateColumn.find_date_cols() method in order to find all datetime columns.
        Then it will display a Streamlit select box with the list of datetime columns found.
        Once the user select a datetime column from the select box, it will call the tab_date.logics.DateColumn.set_data() method in order to compute all the information to be displayed.
        Then it will display a Streamlit Expander container with the following contents:
            - the results of tab_date.logics.DateColumn.get_summary() as a Streamlit Table
            - the graph from tab_date.logics.DateColumn.histogram using Streamlit.altair_chart()
            - the results of tab_date.logics.DateColumn.frequent using Streamlit.write
 
    --------------------
    Parameters
    --------------------
    -> file_path (str): File path to uploaded CSV file (optional)
    -> df (pd.DataFrame): Loaded dataframe (optional)

    --------------------
    Returns
    --------------------
    -> None

    """
    # instatiate a DateColumn object and save it into streamlit session state 
    datecolumn = DateColumn(file_path=file_path, df=df) 
    st.session_state["date_column"] = datecolumn 
    # find all datetime columns 
    datecolumn.find_date_cols() 
    datecols = datecolumn.cols_list 
    # display streamlit select box with list of datetime columns 
    while datecolumn.is_series_none():
        if datecols: 
            datecol = st.selectbox(
                label="Which datetime column do you want to explore?",
                options=datecols, 
                help="Click on which datetime column you'd like to explore further."
            )
            st.session_state["selected_date_col"] = datecol
        else: 
            st.write("No datetime columns could be found.") 
            return None 
        # call set_data() method to assign selected column 
    # --bug: will try to call this before user has selected datecol
    # --fix: run these lines only when a datecol is selected
        datecolumn.set_data(datecol) 
    # # if series is still none 
    # if datecolumn.is_series_none(): 
    #     # remove column from list
    #     datecolumn.cols_list.remove(datecol) 
    #     # and raise an error message
    #     st.error(f"""
    #                 The {datecol} column is empty.
    #                 Please try another selection instead.
    #                 """)


    # # check if the column is empty 
    # if datecolumn.is_series_none(): 
    #     # if so, remove from cols_list
    #     datecolumn.cols_list.remove(datecol) 

    # create the streamlit expander container
    if not datecolumn.is_series_none():
        with st.expander("## Date Column", expanded=True): 
            # display the table 
            st.table(datecolumn.get_summary())
            # display the bar chart 
            st.write("### Bar Chart") 
            st.altair_chart(datecolumn.barchart, use_container_width=True)
            # display frequency table 
            st.write("### Most Frequent Values")
            # create a new session_state parameter for n to check whether it changes 
            if 'n' not in st.session_state: 
                st.session_state.n = 20 

            # display number input widget 
            ## define default value as either datecolumn.n_unique or 20, depending on which is bigger 
            if datecolumn.n_unique < 20:
                value = datecolumn.n_unique 
            else: 
                value = 20 

            n = st.number_input(
                label="Number of most frequent values", 
                min_value=1,
                max_value=datecolumn.n_unique,
                value=value
            )
            # check if value of n has changed from default 
            if n != st.session_state.n: 
                # if so call .set_frequent to update end parameter
                datecolumn.set_frequent(end=n) 
                # and update session_state.n to new value 
                st.session_state.n = n 
            
            # display the dataframe 
            st.dataframe(
                datecolumn.frequent,
                use_container_width=True)