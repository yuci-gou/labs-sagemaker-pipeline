import pandas as pd

# Load the dataset
df = pd.read_csv("data/iris_dataset.csv")

# Drop the 'Id' column
df = df.drop(columns=["Id"])

# Convert the 'Species' column to numeric labels
df["Species"] = df["Species"].map(
    {"Iris-setosa": 0, "Iris-versicolor": 1, "Iris-virginica": 2}
)

# Save the preprocessed data to CSV
df.to_csv("data/iris_preprocessed.csv", index=False)
