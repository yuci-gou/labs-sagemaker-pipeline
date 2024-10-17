import pandas as pd

# Load the dataset
df = pd.read_csv(
    "data/train.csv",
    header=None,
    names=["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm", "Species"],
)

# Check unique values in the 'Species' column
print(df["Species"].unique())

# Check data type of 'Species' column
print(df["Species"].dtype)
