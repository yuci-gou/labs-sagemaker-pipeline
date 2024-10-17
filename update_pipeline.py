import sagemaker
from sagemaker.workflow.steps import TrainingStep, CreateModelStep, ProcessingStep
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput
from sagemaker.inputs import TrainingInput
from sagemaker.estimator import Estimator
from sagemaker.model import Model
from sagemaker.workflow.pipeline_context import PipelineSession
import boto3

# Initialize SageMaker session
session = sagemaker.Session()
pipeline_session = PipelineSession()

# Specify the AWS IAM Role with necessary permissions
role = "arn:aws:iam::222497738794:role/AmazonSageMakerFullAccess"  # Replace with your SageMaker execution role ARN

# S3 bucket where your dataset is located
bucket = "yuci-gc-labs"  # Replace with your S3 bucket
prefix = "sagemaker/iris"  # S3 prefix to store model artifacts

# Training data path in S3
train_data_uri = (
    f"s3://{bucket}/{prefix}/train.csv"  # Ensure you have uploaded the train.csv file
)

# 1. SageMaker Processing Job to Inspect Dataset
script_processor = ScriptProcessor(
    image_uri=sagemaker.image_uris.retrieve(
        framework="sklearn",
        region=session.boto_region_name,
        version="1.0-1",  # Supported sklearn version
    ),
    command=["python3"],
    instance_type="ml.m5.large",
    instance_count=1,
    role=role,
    sagemaker_session=session,
)

# Define a Python script to inspect the data (write this as inspect_data.py)
with open("inspect_data.py", "w") as f:
    f.write(
        """
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
"""
    )

# Define the Processing Step
step_inspect_data = ProcessingStep(
    name="InspectDataStep",
    processor=script_processor,
    inputs=[
        ProcessingInput(source=train_data_uri, destination="/opt/ml/processing/input")
    ],
    outputs=[
        ProcessingOutput(
            output_name="processed_data", source="/opt/ml/processing/output"
        )
    ],
    code="inspect_data.py",  # The script you just created
)

# 2. XGBoost Estimator for Training
xgboost_estimator = Estimator(
    image_uri=sagemaker.image_uris.retrieve(
        "xgboost",
        region=session.boto_region_name,
        version="1.5-1",  # Specify a supported XGBoost version
    ),
    instance_type="ml.m5.large",
    instance_count=1,
    role=role,
    output_path=f"s3://{bucket}/{prefix}/output",
    sagemaker_session=session,
)

# Define hyperparameters for the model
xgboost_estimator.set_hyperparameters(
    objective="multi:softmax",  # Use multiclass classification
    num_class=3,  # Ensure this is dynamically set from the inspection step
    num_round=50,  # Number of boosting rounds
    verbosity=3,  # Increase verbosity for more detailed logs
)

# 3. Training Step
train_step = TrainingStep(
    name="XGBoostTrainingStep",
    estimator=xgboost_estimator,
    inputs={"train": TrainingInput(train_data_uri, content_type="csv")},
)

# 4. Model Creation Step
model = Model(
    image_uri=xgboost_estimator.training_image_uri(),
    model_data=train_step.properties.ModelArtifacts.S3ModelArtifacts,
    role=role,
    sagemaker_session=session,
)

create_model_step = CreateModelStep(
    name="CreateXGBoostModelStep",
    model=model,
)

# Define and create/update the SageMaker Pipeline
pipeline = Pipeline(
    name="SimpleXGBoostPipeline-v2",
    steps=[step_inspect_data, train_step, create_model_step],
)

# Create or update the pipeline
pipeline.upsert(role_arn=role)

# Optionally start the pipeline execution
execution = pipeline.start()
print(f"Pipeline started. Execution ARN: {execution.arn}")
