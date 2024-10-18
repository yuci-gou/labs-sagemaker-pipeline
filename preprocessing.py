
import pandas as pd
import os

# Load dataset
df = pd.read_csv("/opt/ml/processing/input/iris.csv")

# Perform basic preprocessing (in this case, no changes, just an example)
df.to_csv("/opt/ml/processing/output/iris_preprocessed.csv", index=False)
print(f"Processed data saved at /opt/ml/processing/output/iris_preprocessed.csv")
