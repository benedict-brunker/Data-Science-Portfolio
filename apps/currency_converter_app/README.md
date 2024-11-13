# Python Currency Convertor

<b>Benedict Brunker</b>

<b>25551995</b>

## Application Description

### What it does

The Python Currency Convertor allows users to quickly and easily find the exchange rate between two currencies. 

The user can find either the latest rate between two currencies by clicking on the "Get Latest Rate" button, or can find the exchange rate on any day since the 4th of January 1999 by first selecting a date with a calendar input widget, and then clicking on the "Get Historical Rate" button. 
The available currencies are shown in the drop-down menus "From Currency" and "To Currency". 

The user can also input an amount in the number selection widget for "Enter the amount to be converted". 
The app will display the conversion rate between the two currencies on that day, as well as the amount of the "From Currency" converted to the "To Currency". 
It will also display the inverse rate, that is, the exchange rate of the "From Currency" relative to the "To Currency". 

The Convertor works by querying the Frankfurter Application Programing Interface (API), which "tracks foreign exchange references rates published by the European Central Bank." (Frankfurter 2024)

### Challenges 

I am happy to say I did not face significant challenges in undertaking this project. 

### Future Improvements 

We hope to improve the application in future by:

<ul> Creating a more visually interesting and dynamic user interface. </ul>
<ul> Drawing on a wider range of data sources to allow conversions between more currencies over a wider date range. 
        Unfortunately the Frankfurter API can only find exchange rates going back to 1999. </ul>
<ul> Allowing the user to see trends in FX rates over time by allowing users to render time-series charts and other instructive visualizations </ul>
<ul> Serving the application continually on a World Wide Web domain. 
        Unfortunately the application as of now must be served from a local machine. 
        Serving the application from a permanent web domain would allow users to access it at any time without running the corresponding source files. </ul>

<h2> Setup </h2>

<h3> Setup Guide </h3>

If you haven't already, download and extracted  the folder dsp_at2_25551995.zip. 
The other files in this folder contain the source code to run and serve the application. 
Ensure the files are stored together in the same directory of your choosing.

<h3> Source Code </h3>

Python 3.12.5. 

<h3> Packages </h3>

The following package needs to be imported: 

<ul> streamlit  1.38.0 </ul>

The following packages native to Python 3.12.5 are also used:
<ul> requests </ul>
<ul> datetime </ul>
<ul> json </ul>

## How to Run the Program
From the command line, run the following:
<ul><b>streamlit run app.py</b></ul>
This should launch your default web browser which will host the application. That's it!


## Project Structure

<ul><b>app.py</b>       
<br>contains the main source code for the application. </ul>

<ul><b>api.py</b>       
<br>
contains a single function get_url that securely fetches a response from an API endpoint and verifies that the connection is successful. </ul>

<ul><b>frankfurter.py</b> 
<br>
contains code for calling the Frankfurter API, fetching a list of available currencies, as well as latest and historical exchange rates. </ul>

<ul><b>currency.py</b> 
<br>
contains functions for rounding the exchange rate to 4 decimal places, finding the inverse exchange rate, and formatting the output to be displayed in the streamlit app. </ul>

## Learn More
<ul>If you'd like to learn more about how the Frankfurter API works, you can <a href="frankfurter.app/docs/">find the documentation here.</a></ul>
<ul>For more on Streamlit, see the <a href="https://streamlit.io/"> relevant documentation here.</a></ul>
<ul>OpenAI's <a href="https://chatgpt.com/">ChatGPT</a> 3.0 was consulted for help with running terminal commands, but not for coding. 

