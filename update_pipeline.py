import sagemaker
from sagemaker.inputs import TrainingInput
from sagemaker.estimator import Estimator
from sagemaker.workflow.steps import TrainingStep
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.pipeline_context import PipelineSession

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
    f"s3://{bucket}/{prefix}/train.csv"  # Ensure the train.csv file is uploaded to S3
)

# 1. Define the XGBoost Estimator
xgboost_estimator = Estimator(
    image_uri=sagemaker.image_uris.retrieve(
        "xgboost", region=session.boto_region_name, version="1.5-1"
    ),
    instance_type="ml.m5.large",
    instance_count=1,
    role=role,
    output_path=f"s3://{bucket}/{prefix}/output",  # Model artifacts will be saved here
    sagemaker_session=session,
)

# Define hyperparameters for XGBoost
xgboost_estimator.set_hyperparameters(
    objective="multi:softmax",  # Use multiclass classification
    num_class=3,  # Number of classes in the dataset (3 for Iris)
    num_round=50,  # Number of boosting rounds
    verbosity=2,  # Increase verbosity for more detailed logs
)

# 2. Define the Training Step in the Pipeline
train_step = TrainingStep(
    name="XGBoostTrainingStep",
    estimator=xgboost_estimator,
    inputs={"train": TrainingInput(train_data_uri, content_type="csv")},
)

# 3. Define and Create the SageMaker Pipeline
pipeline = Pipeline(
    name="SimpleXGBoostPipeline",
    steps=[train_step],
)

# Create or update the pipeline
pipeline.upsert(role_arn=role)

# Optionally start the pipeline execution
execution = pipeline.start()
print(f"Pipeline started. Execution ARN: {execution.arn}")
