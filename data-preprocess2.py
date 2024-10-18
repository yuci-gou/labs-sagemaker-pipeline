import pandas as pd

# Load your dataset (replace with your actual CSV file path)
df = pd.read_csv("data/train.csv", header=None)

# Move the last column to the first position
df = df[[df.columns[-1]] + list(df.columns[:-1])]

# Save the reordered CSV file
df.to_csv("train_reordered.csv", index=False, header=False)

# Display the first few rows to verify
print(df.head())
