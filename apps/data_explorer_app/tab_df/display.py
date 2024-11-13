import streamlit as st
from tab_df.logics import Dataset

def display_tab_df_content(file_path):
    # Instantiate Dataset class
    dataset_instance = Dataset(file_path=file_path)
    dataset_instance.set_data()

    # Check if dataset has been loaded correctly
    if dataset_instance.df is None:
        st.error("Failed to load the dataset. Please make sure the uploaded file is a valid CSV.")
        return

    # Save Dataset instance (not just df) to session state for future access
    st.session_state["dataset"] = dataset_instance  # Assign the entire Dataset instance
    st.session_state["df"] = dataset_instance.df

    # Display summary information
    with st.expander("Dataset Summary"):
        st.subheader("Dataset Overview")
        # Display summary statistics
        st.table(dataset_instance.get_summary())

        # Display the entire dataset or part of it
        st.subheader("Full Dataset Table")
        st.write(dataset_instance.table)

    # Display slider and radio buttons to filter rows
    with st.expander("Explore Dataframe"):
        # Number of rows to display
        num_rows = st.slider("Select number of rows to be displayed", min_value=5, max_value=50, value=5)
        # Radio button to select head, tail, or random sample
        display_option = st.radio("Exploration Method", options=["Head", "Tail", "Sample"])

        if display_option == "Head":
            st.dataframe(dataset_instance.get_head(num_rows))
        elif display_option == "Tail":
            st.dataframe(dataset_instance.get_tail(num_rows))
        elif display_option == "Sample":
            st.dataframe(dataset_instance.get_sample(num_rows))
