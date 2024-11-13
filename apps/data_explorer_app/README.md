# Collaborative Development of Data Explorer Web App

## Authors
Group 2 : 
- Benedict Brunker (25551995)
- Yuzhong Wang (13123157)
- Justin Govanxa (25153673)
- Britney Rosalia Odria (14131609)

## Description

### Application Description 
Our project was to develop an interactive data explorer web application, designed to help users explore and analyse their datasets.  
It provides a simple, accessible tool for quickly obtaining a general overview of the user’s data and providing useful high-level analysis, allowing users to gain insights into their data. 

### Challenges Faced 
- Testing and debugging the application. 
- Ensuring consistent Python environments and testing files. 
- Agreement on software. 
- External commitments and scheduling. 

### Future Improvements 
- Handling real-time data uploads from API web queries. 
- Handling wider range of file formats. 
- Handling varied data formatting conventions and anomalies. 
- Including wider range of application features for exploring data relationships. 


## How to Setup

### Packages and Versions 
Python >= 3.9 
altair==4.2.0
pandas==2.0.3
streamlit==1.13.0
numpy==1.24.0

## How to Run the Program
1. 	Ensure Python 3.9 or higher is installed on your device. If not, install it from its official website:
Download Python | Python.org
2. 	Open your terminal or command prompt. Navigate to the directory containing your application files, then run the following command to install the required libraries:
pip install -r requirement.txt 
3.	From the same directory, run the following command to launch the application:
streamlit run app/streamlit_app.py

## Project Structure
### Folder Structure

```
DSP_AT3_Group2/ 
    app/    
        __init__.py 
        streamlit_app.py    
    tab_date/  
        __init__.py 
        display.py  
        logics.py   
    tab_df/ 
        __init__.py 
        display.py
        logics.py
    tab_num/ 
        __init__.py
        display.py
        logics.py
    tab_text/ 
        __init__.py
        display.py
        logics.py
    test/  
    94692_DSP_AT3_Report_Group2.docx 
    README.md
    requirements.txt

```

### Explanation 
#### DSP_AT3_Group2 
This is the top-level application folder. 

#### app 
This folder contains source code for running the main architecture of the Streamlit app. 
<i>__init__.py</i> is an empty file that allows the folder to be treated as an importable module. 
streamlit_app.py contains the main source code for initializing and running the Streamlit app. 
This is the file to run to launch the program from a command line once you've navigated to app/, with this command: 
<b> streamlit run streamlit_app.py </b> 
Or, from the root project directory, you can run: 
<b> streamlit run app/streamlit_app.py </b> 

#### tab_num

This folder contains source code for managing the Numeric Series tab in the application.

- logics.py defines the NumericColumn class. This class handles operations for columns of numeric data and includes methods for:

    - NumericColumn.find_num_cols(): Identifies all numeric columns in the uploaded CSV using pandas' select_dtypes method and stores them in cols_list.

    - NumericColumn.set_data(): Initializes the series attribute for the selected numeric column and calculates relevant statistics, such as unique values, missing values, mean, standard deviation, and more. It also generates a histogram and determines the most frequent values.

    - NumericColumn.convert_serie_to_num(): Converts the series to numeric, coercing errors to NaN.

    - The class also includes methods like set_unique(), set_missing(), set_mean(), set_std(), and set_histogram() to compute and store various statistics and visualizations.

- display.py defines the function display_tab_num_content(), which manages the user interface of the Numeric Series tab in the Streamlit app:
    - Initializes a NumericColumn instance with the uploaded DataFrame.
    - Provides a dropdown to select a numeric column to explore.
    - Displays a summary table with key statistics of the selected column.
    - Visualizes the column's distribution using a histogram.
    - Shows a table of the most frequent values.

- \__init__.py configures NumericColumn and display_tab_num_content as importable modules for use in the application. ​

#### tab_text

This folder contains source code for managing the Text Series tab in the application.

- logics.py
logics.py defines the TextColumn class, which is responsible for handling and analyzing text column data. Key methods include:

    - TextColumn.find_text_cols(): Identifies all text columns in the uploaded CSV file. This method classifies columns with an object data type as text columns and stores them in the cols_list attribute.

    - TextColumn.set_data(): For a user-selected text column, this method invokes several auxiliary methods to compute data attributes, storing results in the various attributes of TextColumn. The analysis includes calculating the number of unique values, missing values, empty strings, rows containing only whitespaces, rows with all lowercase or uppercase characters, rows with only alphabetic or numeric characters, and identifying the mode of the column.

    - TextColumn.convert_serie_to_text(): Converts the selected column to text type to ensure compatibility for further string-based analysis.

    - TextColumn.set_barchart(): Creates a bar chart using Altair to visualize the frequency distribution of unique values in the selected text column.

    - TextColumn.set_frequent(): Computes and stores the top 20 most frequent values in the selected column, along with their counts and percentages.

    - TextColumn.get_summary(): Generates a summary table of key statistics for the selected text column, for display in the application.

- display.py
display.py defines the function display_tab_text_content(), which manages the interface for the Text Series tab in the Streamlit application, including:
    - A selection box that allows the user to choose a text column for analysis.
    - A table summarizing key statistics about the selected text column.
    - A bar chart visualizing the distribution of values in the selected column.
    - A table listing the most frequent values in the selected text column, showing their counts and proportions within the dataset.

#### tab_date 

This folder contains source code for managing the <i>Datetime Series</i> tab in the application. 

- <b>logics.py</b> defines the <b>DateColumn</b> class. This class contains some key methods: 

    - <i>DateColumn.find_date_cols()</i> is designed to find all datetime columns in the uploaded csv. If no datetime columns were read in automatically by <i>tab_df.logics.Dataset.set_df</i>, find_date_cols() will find plausible candidates for datetime columns by matching column names to Regular Expressions (RegEx) and then attempt to convert these to datetime with <i>DateColumn.convert_series_to_date()</i>. If there are still no datetime columns, the method finds text columns instead.

    - <i>DateColumn.set_data()</i> calls several subsidiary methods to compute the data to be displayed in the Streamlit app. These data are stored in DateColumn's attributes.  

- <b>display.py</b> defines a function <i>display_tab_date_content()</i> that handles the interface of the <i>Datetime Series</i> tab of the Streamlit app, including: 
    - A selectbox allowing the user to select a datetime column to explore. 
    - A table summarizing key information about the column.  
    - A histogram visualizing the distribution of the selected column. 
    - A chart showing the most frequent values of the column and their proportion of the dataset. 

- <b> \__init__.py </b> configures <i>DateColumn</i> and <i>display_tab_date_content</i> as importable Python modules. 

