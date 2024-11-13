import streamlit as st
from tab_text.logics import TextColumn

def display_tab_text_content(file_path=None, df=None):
    if "text_column_instance" not in st.session_state:
        st.session_state["text_column_instance"] = TextColumn(file_path=file_path, df=df)
    
    text_column = st.session_state["text_column_instance"]
    text_column.find_text_cols()
    
    if not text_column.cols_list:
        st.write("No text columns found in the dataset.")
        return
    
    selected_column = st.selectbox("Select a text column to explore", text_column.cols_list)
    
    if selected_column:
        text_column.set_data(selected_column)
        
        with st.expander("Text Column Summary"):
            summary_df = text_column.get_summary()
            st.table(summary_df)
        
        st.write("### Value Distribution")
        st.altair_chart(text_column.barchart, use_container_width=True)
        
        st.write("### Most Frequent Values")
        st.write(text_column.frequent)
