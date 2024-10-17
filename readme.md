```
python3 -m venv .venv
source .venv/bin/activate
pip install boto3 sagemaker

python3 data-preprocess.py
python3 update_pipeline.py
```

```
(.venv) (base) yucigou@Yucis-MacBook-M2-Pro sagemaker-pipeline % python3 update_pipeline.py
sagemaker.config INFO - Not applying SDK defaults from location: /Library/Application Support/sagemaker/config.yaml
sagemaker.config INFO - Not applying SDK defaults from location: /Users/yucigou/Library/Application Support/sagemaker/config.yaml
INFO:botocore.credentials:Found credentials in environment variables.
INFO:botocore.credentials:Found credentials in environment variables.
INFO:sagemaker.image_uris:Ignoring unnecessary instance type: None.
INFO:botocore.credentials:Found credentials in environment variables.
WARNING:sagemaker.workflow.utilities:Popping out 'TrainingJobName' from the pipeline definition by default since it will be overridden at pipeline execution time. Please utilize the PipelineDefinitionConfig to persist this field in the pipeline definition if desired.
WARNING:sagemaker.workflow.utilities:Popping out 'ModelName' from the pipeline definition by default since it will be overridden at pipeline execution time. Please utilize the PipelineDefinitionConfig to persist this field in the pipeline definition if desired.
Pipeline started. Execution ARN: arn:aws:sagemaker:eu-west-1:222497738794:pipeline/SimpleXGBoostPipeline/execution/ztefwbnlgoif
```

```
(.venv) (base) yucigou@Yucis-MacBook-M2-Pro sagemaker-pipeline % aws sagemaker describe-pipeline-execution --pipeline-execution-arn arn:aws:sagemaker:eu-west-1:222497738794:pipeline/SimpleXGBoostPipeline/execution/tt6yey0lezjc

{
    "PipelineArn": "arn:aws:sagemaker:eu-west-1:222497738794:pipeline/SimpleXGBoostPipeline",
    "PipelineExecutionArn": "arn:aws:sagemaker:eu-west-1:222497738794:pipeline/SimpleXGBoostPipeline/execution/ztefwbnlgoif",
    "PipelineExecutionDisplayName": "execution-1729200011911",
    "PipelineExecutionStatus": "Failed",
    "PipelineExperimentConfig": {
        "ExperimentName": "simplexgboostpipeline",
        "TrialName": "ztefwbnlgoif"
    },
    "FailureReason": "Step failure: One or multiple steps failed.",
    "CreationTime": "2024-10-17T22:20:11.852000+01:00",
    "LastModifiedTime": "2024-10-17T22:20:15.359000+01:00",
    "CreatedBy": {
        "IamIdentity": {
            "Arn": "arn:aws:sts::222497738794:assumed-role/AWSReservedSSO_AWSAdministratorAccess_3d1880080bd27f4f/yuci.gou@green-custard.com",
            "PrincipalId": "AROATHTPGCAVENXZXPB5V:yuci.gou@green-custard.com"
        }
    },
    "LastModifiedBy": {
        "IamIdentity": {
            "Arn": "arn:aws:sts::222497738794:assumed-role/AWSReservedSSO_AWSAdministratorAccess_3d1880080bd27f4f/yuci.gou@green-custard.com",
            "PrincipalId": "AROATHTPGCAVENXZXPB5V:yuci.gou@green-custard.com"
        }
    }
}

(.venv) (base) yucigou@Yucis-MacBook-M2-Pro sagemaker-pipeline % aws sagemaker list-pipeline-execution-steps --pipeline-execution-arn arn:aws:sagemaker:eu-west-1:222497738794:pipeline/SimpleXGBoostPipeline/execution/ztefwbnlgoif

{
    "PipelineExecutionSteps": [
        {
            "StepName": "XGBoostTrainingStep",
            "StartTime": "2024-10-17T22:20:12.859000+01:00",
            "EndTime": "2024-10-17T22:20:15.044000+01:00",
            "StepStatus": "Failed",
            "FailureReason": "ClientError: Failed to invoke sagemaker:CreateTrainingJob. Error Details: The requested resource training-job/ml.t3.medium is not available in this region\nRetry not appropriate on execution of step with PipelineExecutionArn arn:aws:sagemaker:eu-west-1:222497738794:pipeline/simplexgboostpipeline/execution/ztefwbnlgoif and StepId XGBoostTrainingStep. No retry policy configured for the exception type SAGEMAKER_RESOURCE_LIMIT.",
            "Metadata": {},
            "AttemptCount": 1
        }
    ]
}
```
