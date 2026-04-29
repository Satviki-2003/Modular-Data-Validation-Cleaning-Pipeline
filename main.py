from src import reader,validator,reporter,outlier_engine
import json

# Loading the file
loader=reader.DataLoader('./data/input/Employee_dataset.csv')
df=loader.read_data()
print(f"Shape of original data: {df.shape}")

# Segregating data
config=json.load(open('./config.json'))
validator_obj=validator.Validator(df,config)
validator_obj.validate_data()

print(validator_obj.clean_df.head())
print(validator_obj.quarantine_df.head())

print(f"Clean data:{validator_obj.clean_df.shape}")
print(f"Quarantined: {validator_obj.quarantine_df.shape}")

# Reporter
reporter_obj=reporter.Reporter(validator_obj.clean_df,validator_obj.quarantine_df,df.shape[0],config)
reporter_obj.save_quarantine('./data/quarantine/quarantine.csv')

# Outlier handling
outlier_engine_obj=outlier_engine.OutlierEngine(validator_obj.clean_df,config)
outlier_engine_obj.handle_outliers()

reporter_obj.clean_df= outlier_engine_obj.df
reporter_obj.save_cleaned('./data/output/cleaned.csv')

print(f"Clean data:{validator_obj.clean_df.shape}")
print(f"Quarantined: {validator_obj.quarantine_df.shape}")

reporter_obj.generate_report('./data/output/report.txt')