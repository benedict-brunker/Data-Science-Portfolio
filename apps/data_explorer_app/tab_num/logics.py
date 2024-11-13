import pandas as pd
import altair as alt

class NumericColumn:
    """
    --------------------
    Description
    --------------------
    -> NumericColumn (class): Class that manages a column of numeric data type
    --------------------
    Attributes
    --------------------
    -> df (pd.DataFrame): Pandas dataframe (mandatory)
    -> cols_list (list): List of columns names of dataset that are numeric type (default set to empty list)
    -> serie (pd.Series): Pandas series where the content of a column has been loaded (default set to None)
    -> n_unique (int): Number of unique value of a series (default set to None)
    -> n_missing (int): Number of missing values of a series (default set to None)
    -> col_mean (float): Average value of a series (default set to None)
    -> col_std (float): Standard deviation value of a series (default set to None)
    -> col_min (float): Minimum value of a series (default set to None)
    -> col_max (float): Maximum value of a series (default set to None)
    -> col_median (float): Median value of a series (default set to None)
    -> n_zeros (int): Number of times a series has values equal to 0 (default set to None)
    -> n_negatives (int): Number of times a series has negative values (default set to None)
    -> histogram (alt.Chart): Altair histogram displaying the count for each bin value of a series (default set to empty)
    -> frequent (pd.DataFrame): DataFrame containing the most frequent value of a series (default set to empty)
    """

    def __init__(self, file_path=None, df=None):
        # Only load from file_path if it's a non-empty string and ignore if df is provided directly
        if file_path is not None and isinstance(file_path, str):
            self.df = pd.read_csv(file_path)
        elif isinstance(df, pd.DataFrame):
            self.df = df
        else:
            raise ValueError("Either a valid file_path or a DataFrame must be provided.")

        # Initialize other attributes, such as numeric columns
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.col_mean = None
        self.col_std = None
        self.col_min = None
        self.col_max = None
        self.col_median = None
        self.n_zeros = None
        self.n_negatives = None
        self.histogram = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])


    def find_num_cols(self):
        """
        Find all numeric columns in the provided DataFrame and store them in cols_list.
        """
        if self.df is not None:
            self.cols_list = self.df.select_dtypes(include='number').columns.tolist()

    def set_data(self, col_name):
        """
        Set the series attribute to the selected numeric column and compute relevant statistics.
        """
        if self.df is not None and col_name in self.df.columns:
            self.serie = self.df[col_name]
            self.convert_serie_to_num()
            self.set_unique()
            self.set_missing()
            self.set_mean()
            self.set_std()
            self.set_min()
            self.set_max()
            self.set_median()
            self.set_zeros()
            self.set_negatives()
            self.set_histogram()
            self.set_frequent()

    def convert_serie_to_num(self):
        """
        Convert the series to numeric values, coercing errors to NaN.
        """
        if self.serie is not None:
            self.serie = pd.to_numeric(self.serie, errors='coerce')

    def is_serie_none(self):
        """
        Check if the series is None or empty.
        """
        return self.serie is None or self.serie.empty

    def set_unique(self):
        if not self.is_serie_none():
            self.n_unique = self.serie.nunique()

    def set_missing(self):
        if not self.is_serie_none():
            self.n_missing = self.serie.isna().sum()

    def set_zeros(self):
        if not self.is_serie_none():
            self.n_zeros = (self.serie == 0).sum()

    def set_negatives(self):
        if not self.is_serie_none():
            self.n_negatives = (self.serie < 0).sum()

    def set_mean(self):
        if not self.is_serie_none():
            self.col_mean = self.serie.mean()

    def set_std(self):
        if not self.is_serie_none():
            self.col_std = self.serie.std()

    def set_min(self):
        if not self.is_serie_none():
            self.col_min = self.serie.min()

    def set_max(self):
        if not self.is_serie_none():
            self.col_max = self.serie.max()

    def set_median(self):
        if not self.is_serie_none():
            self.col_median = self.serie.median()

    def set_histogram(self):
        """
        Create an Altair histogram for the numeric series if it's valid.
        """
        if not self.is_serie_none():
            self.histogram = alt.Chart(self.df).mark_bar().encode(
                alt.X(f"{self.serie.name}:Q", bin=True),
                y='count()'
            ).properties(
                width=600,
                height=400
            )

    def set_frequent(self, end=20):
        """
        Create a DataFrame of the most frequent values in the series.
        """
        if not self.is_serie_none():
            value_counts = self.serie.value_counts().head(end).reset_index()
            value_counts.columns = ['value', 'occurrence']
            value_counts['percentage'] = (value_counts['occurrence'] / len(self.serie)) * 100
            self.frequent = value_counts

    def get_summary(self):
        """
        Get a summary of statistics for the numeric series.
        """
        if not self.is_serie_none():
            summary = {
                "Description": [
                    "Number of Unique Values",
                    "Number of Missing Values",
                    "Number of Rows with 0 Value",
                    "Number of Negative Values",
                    "Average Value",
                    "Standard Deviation",
                    "Minimum Value",
                    "Maximum Value",
                    "Median Value"
                ],
                "Value": [
                    self.n_unique,
                    self.n_missing,
                    self.n_zeros,
                    self.n_negatives,
                    self.col_mean,
                    self.col_std,
                    self.col_min,
                    self.col_max,
                    self.col_median
                ]
            }
            return pd.DataFrame(summary)
        return pd.DataFrame(columns=["Description", "Value"])
