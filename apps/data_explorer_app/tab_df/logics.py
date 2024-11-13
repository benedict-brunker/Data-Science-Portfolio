import pandas as pd

class Dataset:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.cols_list = []
        self.n_rows = 0
        self.n_cols = 0
        self.n_duplicates = 0
        self.n_missing = 0
        self.n_num_cols = 0
        self.n_text_cols = 0
        self.table = None

    def set_data(self):
        self.set_df()
        if not self.is_df_none():
            self.set_columns()
            self.set_dimensions()
            self.set_duplicates()  
            self.set_missing()      
            self.set_numeric()      
            self.set_text()         
            self.set_table()

    def set_df(self):
        if self.df is None:
            self.df = pd.read_csv(self.file_path)

    def is_df_none(self):
        return self.df is None or self.df.empty

    def set_columns(self):
        if not self.is_df_none():
            self.cols_list = list(self.df.columns)

    def set_dimensions(self):
        if not self.is_df_none():
            self.n_rows, self.n_cols = self.df.shape

    def set_duplicates(self):
        if not self.is_df_none():
            self.n_duplicates = self.df.duplicated().sum()

    def set_missing(self):
        if not self.is_df_none():
            self.n_missing = self.df.isnull().sum().sum()

    def set_numeric(self):
        if not self.is_df_none():
            self.n_num_cols = self.df.select_dtypes(include='number').shape[1]

    def set_text(self):
        if not self.is_df_none():
            self.n_text_cols = self.df.select_dtypes(include='object').shape[1]

    def get_head(self, n=5):
        if not self.is_df_none():
            return self.df.head(n)

    def get_tail(self, n=5):
        if not self.is_df_none():
            return self.df.tail(n)

    def get_sample(self, n=5):
        if not self.is_df_none():
            return self.df.sample(n)

    def set_table(self):
        if not self.is_df_none():
            self.table = pd.DataFrame({
            'column': self.df.columns,
            'data_type': self.df.dtypes.values, 
            'memory': self.df.memory_usage(deep=True, index=False).values  
        })


    def get_summary(self):
        summary = {"Description": [
            "Number of Rows", "Number of Columns", "Number of Duplicated Rows", "Number of Rows with Missing Values"
            ],
             "Value": [
            self.n_rows, self.n_cols, self.n_duplicates, self.n_missing
            ]
            }
        return pd.DataFrame(summary)