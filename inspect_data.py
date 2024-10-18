
import pandas as pd

# Load the dataset without headers
df = pd.read_csv("/opt/ml/processing/input/train.csv", header=None)

# Assign column names manually, matching the data format
df.columns = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species']

# Print out the first few rows to inspect
print("First few rows of the training data:")
print(df.head())

# Check if the labels are correct and within the expected range
print("Unique labels in the 'Species' column:")
print(df['Species'].unique())

# Save the number of unique classes to a file
with open("/opt/ml/processing/output/num_classes.txt", "w") as out_file:
    out_file.write(str(df['Species'].nunique()))
