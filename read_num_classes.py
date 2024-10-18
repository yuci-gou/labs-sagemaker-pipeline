
# This script reads num_classes from the file and outputs it.
with open('/opt/ml/processing/input/num_classes.txt', 'r') as f:
    num_classes = int(f.read())
    print(f"Number of classes detected: {num_classes}")
        