import pandas as pd
import altair as alt

class TextColumn:
    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = pd.read_csv(file_path) if file_path else df
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.n_empty = None
        self.n_mode = None
        self.n_space = None
        self.n_lower = None
        self.n_upper = None
        self.n_alpha = None
        self.n_digit = None
        self.barchart = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])

    def find_text_cols(self):
        self.cols_list = [col for col in self.df.columns if self.df[col].dtype == 'object']

    def set_data(self, col_name):
        self.serie = self.df[col_name].fillna('')
        self.convert_serie_to_text()
        self.set_unique()
        self.set_missing()
        self.set_empty()
        self.set_mode()
        self.set_whitespace()
        self.set_lowercase()
        self.set_uppercase()
        self.set_alphabet()
        self.set_digit()
        self.set_barchart()
        self.set_frequent()

    def convert_serie_to_text(self):
        self.serie = self.serie.astype(str)

    def is_serie_none(self):
        return self.serie is None or self.serie.empty

    def set_unique(self):
        self.n_unique = self.serie.nunique()

    def set_missing(self):
        self.n_missing = self.serie.isna().sum()

    def set_empty(self):
        self.n_empty = (self.serie == '').sum()

    def set_mode(self):
        self.n_mode = self.serie.mode()[0] if not self.serie.mode().empty else None

    def set_whitespace(self):
        self.n_space = self.serie.str.isspace().sum()

    def set_lowercase(self):
        self.n_lower = self.serie.str.islower().sum()

    def set_uppercase(self):
        self.n_upper = self.serie.str.isupper().sum()

    def set_alphabet(self):
        self.n_alpha = self.serie.str.isalpha().sum()

    def set_digit(self):
        self.n_digit = self.serie.str.isdigit().sum()

    def set_barchart(self):
        value_counts = self.serie.value_counts().reset_index()
        value_counts.columns = ['value', 'count']
        self.barchart = alt.Chart(value_counts).mark_bar().encode(
            x=alt.X('value:N', title='Value'),
            y=alt.Y('count:Q', title='Count')
        )

    def set_frequent(self, end=20):
        value_counts = self.serie.value_counts().head(end)
        total_count = len(self.serie)
        self.frequent = pd.DataFrame({
            'value': value_counts.index,
            'occurrence': value_counts.values,
            'percentage': (value_counts / total_count).round(4)
        })

    def get_summary(self):
        summary = {
            'Number of Unique Values': self.n_unique,
            'Number of Rows with Missing Values': self.n_missing,
            'Number of Empty Rows': self.n_empty,
            'Number of Rows with Only Whitespaces': self.n_space,
            'Number of Rows with Only Lowercases': self.n_lower,
            'Number of Rows with Only Uppercases': self.n_upper,
            'Number of Rows with Only Alphabet': self.n_alpha,
            'Number of Rows with Only Digits': self.n_digit,
            'Mode Value': self.n_mode
        }
        return pd.DataFrame(list(summary.items()), columns=["Description", "Value"])
