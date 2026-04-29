import pandas as pd

class Validator:
  def __init__(self, df, config):
    self.df=df
    self.config=config

  def validate_data(self):
    self.clean_df = self.df.copy()
    self.quarantine_df = pd.DataFrame()
    
    for column, obj in self.config.items():
      if column not in self.df.columns:
        print(f"Column {column} not found in the dataframe")
        continue
        
      rule=obj.get("rule")
      nulls=obj.get("nulls")
      
      if nulls.lower()=='mean':
        mean_value=self.clean_df[column].mean()
        self.clean_df.fillna({column:mean_value},inplace=True)
      elif nulls.lower()=='median':
        median_value=self.clean_df[column].median()
        self.clean_df.fillna({column:median_value},inplace=True)
      elif nulls.lower()=='mode':
        mode_value=self.clean_df[column].mode()[0]
        self.clean_df.fillna({column:mode_value},inplace=True)
      elif pd.api.types.is_string_dtype(self.clean_df[column]):
        self.clean_df.fillna({column: nulls}, inplace=True)
      elif pd.api.types.is_bool_dtype(self.clean_df[column]):
        self.clean_df.fillna({column: bool(nulls)}, inplace=True)
      else:
        self.clean_df.fillna({column:float(nulls)},inplace=True)
      
      if rule:
        check_series = self.clean_df[column].astype(str).str.strip()
        is_valid=check_series.astype(str).str.match(rule).fillna(True)

        quarantine_rows=self.clean_df[~is_valid]
        self.quarantine_df=pd.concat([self.quarantine_df,quarantine_rows],ignore_index=True)
        self.clean_df=self.clean_df[is_valid]
        
    # Handling duplicates
    self.clean_df=self.clean_df.drop_duplicates()
    self.quarantine_df=self.quarantine_df.drop_duplicates()

    # reset indexes
    self.clean_df.reset_index(drop=True, inplace=True)
    self.quarantine_df.reset_index(drop=True, inplace=True)
    
    return    