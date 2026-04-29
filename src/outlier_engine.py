import pandas as pd

class OutlierEngine:

  def __init__(self,df,config):
     self.df=df
     self.config=config

  def handle_outliers(self):
    for column, obj in self.config.items():
      if column not in self.df.columns:
        print(f"Column {column} not found in the dataframe")
        continue

      if "outliers" not in obj:
        continue

      q1=self.df[column].quantile(0.25)
      q3=self.df[column].quantile(0.75)
      iqr=q3-q1
      lower_bound=q1-1.5*iqr
      upper_bound=q3+1.5*iqr

      if obj["outliers"].lower()=="cap":
         if pd.api.types.is_numeric_dtype(self.df[column]):
           self.df[column]=self.df[column].clip(lower_bound,upper_bound)

      elif obj["outliers"].lower()=="drop":
        self.df = self.df[(self.df[column] >= lower_bound) & (self.df[column] <= upper_bound)]
        self.df.reset_index(drop=True, inplace=True)

    return