import pandas as pd
import os

class DataLoader:
  def __init__(self, file_path):
    self.filepath = file_path

  def read_data(self):
    extension=os.path.splitext(self.filepath)[1]

    if not os.path.exists(self.filepath):
      print(f"File not found :{self.filepath}")
      return None
    elif extension == '.csv':
      return pd.read_csv(self.filepath)
    elif extension == '.xlsx':
      return pd.read_excel(self.filepath)
    else:
      print("Unsupported file format. Please provide a CSV or Excel file.")
      return None