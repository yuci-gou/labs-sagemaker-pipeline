
import pandas as pd

# Load the dataset without headers
df = pd.read_csv("/opt/ml/processing/input/train.csv", header=None)

# Assign column names manually, matching the data format
df.columns = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species']

# Check for missing values or inconsistencies
print("Checking for missing values:")
print(df.isnull().sum())

# Ensure the label column 'Species' is of type integer
df['Species'] = df['Species'].astype(int)
print(df.dtypes)

# Print out the first few rows to inspect
print("First few rows of the training data:")
print(df.head())

# Check if the labels are correct and within the expected range
print("Unique labels in the 'Species' column:")
print(df['Species'].unique())

# Count the number of unique labels
num_classes = len(df['Species'].unique())
print(f"Number of classes: {num_classes}")

# Save this value to use later in training step (e.g., you could write this to S3 or output it for the training script)
with open("/opt/ml/processing/output/num_classes.txt", "w") as f:
    f.write(str(num_classes))
