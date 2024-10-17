import pandas as pd

# Load the dataset
df = pd.read_csv("data/train.csv", header=None)

# Verify the number of columns
print(df.shape)  # Should return (n_rows, 5)
