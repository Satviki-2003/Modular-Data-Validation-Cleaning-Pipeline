import pandas as pd

class Reporter:
  def __init__(self,clean_df,quarantine_df,initial_count,config):
      self.clean_df=clean_df
      self.quarantine_df=quarantine_df
      self.initial_count = initial_count
      self.config=config

  def save_quarantine(self,path):
    self.quarantine_df.to_csv(path,index=False)

  def save_cleaned(self,path):
    self.clean_df.to_csv(path,index=False)

  def generate_report(self,path):
    with open(path,'w') as f:
      f.write("=== DATA PIPELINE EXECUTIVE SUMMARY ===\n")
      f.write(f"Total Records Input: {self.initial_count}\n")
      f.write(f"Cleaned Records:     {len(self.clean_df)}\n")
      f.write(f"Quarantined Records: {len(self.quarantine_df)}\n")

      success_rate = (len(self.clean_df) / self.initial_count) * 100
      f.write(f"Pipeline Success Rate: {success_rate:.2f}%\n")

      f.write("\n=== COLUMN SUMMARY ===\n")

      # Loop through only the columns defined in the config
      for column in self.config.keys():
          if column in self.clean_df.columns:
              col_data = self.clean_df[column]

              # If it's numeric, give Mean/Median
              if pd.api.types.is_numeric_dtype(col_data):
                  f.write(f"[{column.upper()}]\n")
                  f.write(f"  - Average: {col_data.mean():.2f}\n")
                  f.write(f"  - Median:  {col_data.median():.2f}\n")

              # If it's a string/object, give the most common value (Mode)
              else:
                  f.write(f"[{column.upper()}]\n")
                  mode_val = col_data.mode()[0] if not col_data.mode().empty else "N/A"
                  f.write(f"  - Most Frequent: {mode_val}\n")
                  f.write(f"  - Unique Values: {col_data.nunique()}\n")

      f.write("\n=== VALIDATION RULES APPLIED ===\n")
      for column, obj in self.config.items():
          rule_type = "Regex" if obj.get("rule") else "Type Check"
          impute_type = obj.get("nulls", "None")
          f.write(f"- {column}: Validated via {rule_type}, Nulls handled as '{impute_type}'\n")

      print(f"Report successfully generated at: {path}")
  