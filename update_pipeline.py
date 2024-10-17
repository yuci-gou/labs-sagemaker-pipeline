import sagemaker
from sagemaker.workflow.steps import TrainingStep, CreateModelStep
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.inputs import TrainingInput
from sagemaker.estimator import Estimator
from sagemaker.model import Model
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.workflow.execution_variables import ExecutionVariables
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

# Define XGBoost estimator for training
xgboost_estimator = Estimator(
    image_uri=sagemaker.image_uris.retrieve(
        "xgboost",
        region=session.boto_region_name,
        version="1.5-1",  # Specify a supported XGBoost version
    ),
    instance_type="ml.t3.medium",
    instance_count=1,
    role=role,
    output_path=f"s3://{bucket}/{prefix}/output",
    sagemaker_session=session,
)


# Define hyperparameters for the model (very simple parameters for a demo)
xgboost_estimator.set_hyperparameters(
    objective="binary:logistic",  # A simple binary classification task
    num_round=50,  # Number of rounds for boosting
)

# Define the Training Step in the Pipeline
train_step = TrainingStep(
    name="XGBoostTrainingStep",
    estimator=xgboost_estimator,
    inputs={"train": TrainingInput(train_data_uri, content_type="csv")},
)

# Define Model Creation Step
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
pipeline = Pipeline(name="SimpleXGBoostPipeline", steps=[train_step, create_model_step])

# Create or update the pipeline
pipeline.upsert(role_arn=role)

# Optionally start the pipeline execution
execution = pipeline.start()
print(f"Pipeline started. Execution ARN: {execution.arn}")
