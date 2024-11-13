import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime 
import re 

class DateColumn:
    """
    --------------------
    Description
    --------------------
    -> DateColumn (class): Class that manages a column from a dataframe of datetime data type

    --------------------
    Attributes
    --------------------
    -> file_path (str): Path to the uploaded CSV file (optional)
    -> df (pd.Dataframe): Pandas dataframe (optional)
    -> cols_list (list): List of columns names of dataset that are text type (default set to empty list)
    -> series (pd.Series): Pandas series where the content of a column has been loaded (default set to None)
    -> n_unique (int): Number of unique value of a series (optional)
    -> n_missing (int): Number of missing values of a series (optional)
    -> col_min (int): Minimum value of a series (optional)
    -> col_max (int): Maximum value of a series (optional)
    -> n_weekend (int): Number of times a series has dates falling during weekend (optional)
    -> n_weekday (int): Number of times a series has dates not falling during weekend (optional)
    -> n_future (int): Number of times a series has dates falling in the future (optional)
    -> n_empty_1900 (int): Number of times a series has dates equal to '1900-01-01' (optional)
    -> n_empty_1970 (int): Number of times a series has dates equal to '1970-01-01' (optional)
    -> barchart (int): Altair barchart displaying the count for each value of a series (optional)
    -> frequent (int): Dataframe containing the most frequest value of a series (optional)

    """
    # when the class is initialized, it will take the df from the session_state of streamlit_app.py 
    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = df
        self.cols_list = []
        self.series = None
        self.n_unique = None
        self.n_missing = None
        self.col_min = None
        self.col_max = None
        self.n_weekend = None
        self.n_weekday = None
        self.n_future = None
        self.n_empty_1900 = None
        self.n_empty_1970 = None
        self.barchart = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])
    
    def find_date_cols(self):
        """
        --------------------
        Description
        --------------------
        -> find_date_cols (method): 
            Class method that will load the uploaded CSV file as Pandas DataFrame and store it as attribute (self.df) if it hasn't been provided before.
            Then it will find all columns of datetime data type. 
                If it can't find any datetime then it will look for all columns of text type. 
                Then it will store the results in the relevant attribute (self.cols_list).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        # if no argument is passed to df (no df loaded in session_state) but there is an argument passed to filepath 
        if self.df is None and self.file_path is not None: 
            # load the csv in file_path into the self.df attribute
            self.df = pd.read_csv(self.file_path) 

        dt_types = [np.datetime64, 'datetime', 'datetime64']
        self.cols_list = self.df.select_dtypes(include=dt_types).columns.tolist() 
        if len(self.cols_list) < 1: 
            # try to find integer dtypes that are really years 
            num_cols = self.df.select_dtypes(include='number').columns.tolist() 
            text_cols = self.df.select_dtypes(include='object').columns.tolist() 
            dt_pattern = re.compile(r"year|yr|mon|week|wk|day|dob|date|time|hour|minute|sec", flags=re.IGNORECASE)
            # for each column in numbers, check if the following conditions are satisfied: 
            for col in num_cols: 
                if re.search(dt_pattern, col): 
                    self.cols_list.append(col) 
            # do same for text cols 
            for col in text_cols: 
                if re.search(dt_pattern, col): 
                    self.cols_list.append(col)
            # if resulting cols_list is still empty, extract text type columns 
            if len(self.cols_list) < 1: 
                text_cols = self.df.select_dtypes(include='object')
                self.cols_list = text_cols 
    

    def set_data(self, col_name):
        """
        --------------------
        Description
        --------------------
        --------------------
        Description
        --------------------
        -> set_data (method): 
            Class method that sets the self.series attribute with the relevant column from the dataframe and then computes all requested information from self.series to be displayed in the Date section of Streamlit app 

        --------------------
        Parameters
        --------------------
        -> col_name (str): Name of the text column to be analysed

        --------------------
        Returns
        --------------------
        -> None
        """
        # set self.series to the series for input column name
        self.series = self.df[col_name] 

        # if self.series is not datetime dtype, convert it 
        if self.series.dtype != 'datetime': 
            self.convert_series_to_date()
        
        ## check if series is empty  
        if not self.is_series_none() and col_name in self.df.columns: 
        # compute info by calling on additional methods
            ## compute n_unique values 
            self.set_unique() 

            ## compute n missing values 
            self.set_missing() 

            ## compute min value 
            self.set_min() 

            ## compute max value 
            self.set_max() 

            ## compute number of weekend days 
            self.set_weekend() 

            ## compute number of weekdays 
            self.set_weekday() 

            ## compute number of future dates 
            self.set_future() 

            ## compute number of dates out of range
            self.set_empty_1900() 
            self.set_empty_1970() 

            # compute most frequent values
            self.set_frequent() 

            ## store histogram container 
            self.set_barchart() 

        
        

    def convert_series_to_date(self):
        """
        --------------------
        Description
        --------------------
        -> convert_series_to_date (method): 
            Class method that convert a Pandas Series to datetime data type and store the results in the relevant attribute (self.series).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        # handle year only formats 
        if re.search(r'year', self.series.name, re.IGNORECASE): 
            self.series = pd.to_datetime(self.series.astype(str) + "-01-01", errors='coerce')
            print(self.series.head(10))
        else: 
            self.series = pd.to_datetime(
                self.series, 
                errors='coerce',
                infer_datetime_format=True
                ) 

    def is_series_none(self):
        """
        --------------------
        Description
        --------------------
        -> is_series_none (method): Class method that checks if self.serie is empty or none 

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> (bool): Flag stating if the serie is empty or not

        """
        # return True if series only contains null values 
        if self.series is None or self.series.empty or self.series.isnull().all(): 
            return True 
        else:
            return False 
        
    def set_unique(self):
        """
        --------------------
        Description
        --------------------
        -> set_unique (method): Class method that computes the number of unique value of a serie and store the results in the relevant attribute(self.n_unique).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        self.n_unique = self.series.nunique() 

    def set_missing(self):
        """
        --------------------
        Description
        --------------------
        -> set_missing (method): Class method that computes the number of missing value of a serie and store the results in the relevant attribute(self.n_missing).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        self.n_missing = self.series.isnull().sum() 

    def set_min(self):
        """
        --------------------
        Description
        --------------------
        -> set_min (method): Class method that computes the minimum value of a serie and store the results in the relevant attribute(self.col_min).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        self.col_min = self.series.min() 

    def set_max(self):
        """
        --------------------
        Description
        --------------------
        -> set_max (method): Class method that computes the minimum value of a serie and store the results in the relevant attribute(self.col_max).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        self.col_max = self.series.max() 

    def set_weekend(self):
        """
        --------------------
        Description
        --------------------
        -> set_weekend (method): Class method that computes the number of times a series has dates falling during weekend and store the results in the relevant attribute(self.n_weekend).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        # if all weekdays are the same, the series is likely not denominated in days, so return NA 
        if (self.series.dt.day.nunique() < 2): 
            self.n_weekend = pd.NA 
        # weekdays are represented as 5/6, so count occurrences of these numbers 
        # filter weekend days 
        else: 
            weekdays = self.series.dt.weekday
            weekends = weekdays[weekdays > 4] 
            # then simply find the length of the filtered series to store as the attribute 
            self.n_weekend = len(weekends) 

    def set_weekday(self):
        """
        --------------------
        Description
        --------------------
        -> set_weekday (method): Class method that computes the number of times a serie has dates not falling during weekend and store the results in the relevant attribute(self.n_weekday).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        # if all days are the same, assume series not denominated by days and return NA 
        if (self.series.dt.day.nunique() < 2): 
            self.n_weekday = pd.NA 
        else: 
            weekdays = self.series.dt.weekday 
            self.n_weekday = len(weekdays[weekdays < 5])

    def set_future(self):
        """
        --------------------
        Description
        --------------------
        -> set_future (method): Class method that computes the number of times a series has dates falling in the future and store the results in the relevant attribute(self.n_future).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        # find current datetime  
        now = datetime.now() 
        # filter series for dates after now 
        self.n_future = len(self.series[self.series > now])
    
    def set_empty_1900(self):
        """
        --------------------
        Description
        --------------------
        -> set_empty_1900 (method): Class method that computes the number of times a serie has dates equal to '1900-01-01' and store the results in the relevant attribute(self.n_empty_1900).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        self.n_empty_1900 = self.series[self.series == '1900-01-01'].count() 

    def set_empty_1970(self):
        """
        --------------------
        Description
        --------------------
        -> set_empty_1970 (method): Class method that computes the number of times a series has only digit characters and store the results in the relevant attribute(self.n_empty_1970).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        self.n_empty_1970 = self.series[self.series == '1970-01-01'].count() 

    def set_barchart(self):  
        """
        --------------------
        Description
        --------------------
        -> set_barchart (method): Class method that computes the Altair barchart displaying the count for each value of a series and store the results in the relevant attribute(self.barchart).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if not self.is_series_none():
            # calculate the distribution range in days 
            date_range_days = (self.col_max - self.col_min).days 
            print("Date range in days:", date_range_days)
            # determine correct bin unit based on range 
            if date_range_days > 365:
                # if .n_weekend and .n_weekday are NA, we can assume the data is not denominated in days and so display only the Year
                if pd.isna(self.n_weekend) and pd.isna(self.n_weekday): 
                    self.df['Year'] = self.series.dt.year
                    x_axis = alt.X('Year:O', title="Year") 
                # otherwise we can display the date itself 
                else: 
                    x_axis = alt.X(f'{self.series.name}:T') 
            elif date_range_days > 30: 
                x_axis = alt.X(f'month({self.series.name}):T') 
            elif date_range_days > 7: 
                x_axis = alt.X(f'date({self.series.name}):T')
            else:
                x_axis = alt.X(f'date({self.series.name}):T') 

            self.barchart = alt.Chart(self.df).mark_bar().encode(
                x=x_axis, 
                y='count()',
                tooltip=[alt.Tooltip(f'{self.series.name}:T', title=self.series.name), 'count()']
            ).interactive()
      
    def set_frequent(self, end=20):
        """
        --------------------
        Description
        --------------------
        -> set_frequent (method): Class method that computes the Dataframe containing the most frequest value of a serie and store the results in the relevant attribute(self.frequent).

        --------------------
        Parameters
        --------------------
        -> end (int):
            Parameter indicating the maximum number of values to be displayed

        --------------------
        Returns
        --------------------
        -> None

        """
        # if self.frequent is not empty, reset it 
        if not self.frequent.empty:
            self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])
        VCs = self.series.value_counts() 
        self.frequent['value'] = VCs.index
        self.frequent['occurrence'] = VCs.values
        self.frequent['percentage'] = self.series.value_counts(normalize=True).values
        self.frequent = self.frequent.head(end) 

    def get_summary(self):
        """
        --------------------
        Description
        --------------------
        -> get_summary (method): Class method that formats all requested information from self.serie to be displayed in the Overall section of Streamlit app as a Pandas dataframe with 2 columns: Description and Value

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> (pd.DataFrame): Formatted dataframe to be displayed on the Streamlit app

        """
        # create dataframe with DateColumn attributes as values 
        summary_data = {
            'Number of Unique Values': self.n_unique, 
            'Number of Rows with Missing Values': self.n_missing, 
            'Number of Weekend Dates': self.n_weekend, 
            'Number of Weekday Dates': self.n_weekday, 
            'Number of Dates in Future': self.n_future, 
            'Number of Rows with 1900-01-01': self.n_empty_1900, 
            'Number of Rows with 1970-01-01': self.n_empty_1970, 
            'Minimum Value': self.col_min, 
            'Maximum Value': self.col_max 
        }
        summary_df = pd.DataFrame.from_dict(summary_data, orient='index').reset_index() 
        summary_df.columns = ["Description", "Value"] 
        return summary_df 
