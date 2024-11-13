import streamlit as st
import datetime

from frankfurter import get_currencies_list, get_latest_rates, get_historical_rate
from currency import reverse_rate, round_rate, format_output

# main function
def main():
    # Display Streamlit App Title
    st.title("FX Converter")

    # Get the list of available currencies from Frankfurter
    available_currencies = get_currencies_list()

    # If the list of available currencies is None, display an error message in Streamlit App
    if available_currencies is None:
        st.text("Error 1: Available currencies could not be found from the Frankfurter endpoint")
        print("The function get_currencies_list could not successfully return a list of available currencies from the Frankfurter endpoint.\nExit main program app.py with Error Code 1.")
        return 1

    # Add input fields for capturing amount, from and to currencies
    ## amount
    amount = st.number_input(
        label="Enter the amount to be converted:",
        min_value=1.0,
        value=50.0,
        step=1.0
    )
    ## from currency
    from_currency = st.selectbox(
        label="From Currency:",
        options=available_currencies,
    )
    ## to currency
    to_currency = st.selectbox(
        label="To Currency:",
        options=available_currencies,
        index=29 # indexing to USD as the default rendering
    )
    # Add a button to get and display the latest rate for selected currencies and amount
    if st.button(label="Get Latest Rate"):
        ## if the button is clicked, call the get_latest_rates function
        date_today, rate = get_latest_rates(from_currency, to_currency, amount)
        ## call format_output to find converted amount and inverse rate, and format the output string
        fstring = format_output(date_today, from_currency, to_currency, rate, amount)
        ## display header for Latest Conversion Rate
        st.header("Latest Conversion Rate")
        ## display text providing the conversion rate and date
        st.write(fstring)

    # Add a date selector (calendar)
    from_date = st.date_input(
        label="Select a date for historical rates:",
        value=datetime.date(2000,1,1), 
        min_value=datetime.date(1999,1,4), # this is the earliest allowable date that can be passed to the Frankfurter API
        max_value=datetime.date.today(), # don't allow any date after today. Unforunately this app cannot tell the future!
    )

    # Add a button to get and display the historical rate for selected date, currencies and amount
    if st.button(label="Get Historical Rate"):
        # if the button is clicked, call the get_historical_rate function
        rate = get_historical_rate(from_currency, to_currency, from_date, amount)
        # call format_output to calculate converted amount and inverse rate, and to format the output string
        fstring = format_output(from_date, from_currency, to_currency, rate, amount)
        # Display header
        st.header(f"Conversion Rate for {from_date}")
        # Display the formatted string
        st.write(fstring)

# call main
main()








