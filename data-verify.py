import pandas as pd

# Load the dataset without a header and provide the correct column names
column_names = [
    "SepalLengthCm",
    "SepalWidthCm",
    "PetalLengthCm",
    "PetalWidthCm",
    "Species",
]
df = pd.read_csv("data/train.csv", header=None, names=column_names)

# Print all the column names to confirm
print(df.columns)

# Print unique values in the 'Species' column to verify the labels
print(df["Species"].unique())
